import unittest
from src.fp import (
    Fp,
)
from src.fp2 import (
    Fp2,
)
from src.fp6 import (
    Fp6,
)
from src.fp12 import (
    Fp12,
)
from src.g1 import G1Affine, G1Projective, BETA
from src.g2 import G2Affine, G2Projective
import random
from src.utils import array_to_number, Choice, BLS_X, BLS_X_IS_NEGATIVE
from src.scalar import Scalar


class TestG2(unittest.TestCase):
    def test_identity(self):
        a = G2Projective.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp2.one()) and a.z.is_zero())

    def test_projective_point_equality(self):
        a = G2Projective.generator()
        b = G2Projective.identity()

        self.assertTrue(a.eq(a))
        self.assertTrue(b.eq(b))
        self.assertFalse(a.eq(b))
        self.assertFalse(b.eq(a))

        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )

        c = G2Projective(a.x * z, a.y * z, z)
        self.assertTrue(c.is_on_curve())
        self.assertTrue(a.eq(c))
        self.assertFalse(b.eq(c))
        self.assertTrue(c.eq(a))
        self.assertFalse(c.eq(b))

        c.y = -c.y
        self.assertTrue(c.is_on_curve())
        self.assertFalse(a.eq(c))
        self.assertFalse(b.eq(c))
        self.assertFalse(c.eq(a))
        self.assertFalse(c.eq(b))

        c.y = -c.y
        c.x = z
        self.assertFalse(c.is_on_curve())
        self.assertFalse(a.eq(b))
        self.assertFalse(a.eq(c))
        self.assertFalse(b.eq(c))


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G1Projective.identity().is_on_curve())
        self.assertTrue(G1Projective.generator().is_on_curve())

        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )

        gen = G2Affine.generator()
        test = G2Projective(gen.x * z, gen.y * z, z)
        self.assertTrue(test.is_on_curve())
        test.x = z
        self.assertFalse(test.is_on_curve())


class TestConditionnalSelect(unittest.TestCase):
    def test_conditionally_select_projective(self):
        a = G2Projective.generator()
        b = G2Projective.identity()

        case0 = G2Projective.conditional_select(a, b, Choice(0))
        case1 = G2Projective.conditional_select(a, b, Choice(1))

        self.assertTrue(case0.x.eq(a.x) and case0.y.eq(a.y) and case0.z.eq(a.z))
        self.assertTrue(case1.x.eq(b.x) and case1.y.eq(b.y) and case1.z.eq(b.z))


class TestAffineToProjective(unittest.TestCase):
    def test_affine_to_projective(self):
        a = G2Affine.generator()
        b = G2Affine.identity()

        self.assertTrue(G2Projective.from_g2_affine(a).is_on_curve())
        self.assertFalse(G2Projective.from_g2_affine(a).is_identity())
        self.assertTrue(G2Projective.from_g2_affine(b).is_on_curve())
        self.assertTrue(G2Projective.from_g2_affine(b).is_identity())


class TestDoubling(unittest.TestCase):
    def test_doubling(self):
        tmp = G2Projective.identity().double()
        self.assertTrue(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

        tmp = G2Projective.generator().double()
        self.assertFalse(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

        self.assertTrue(
            G2Affine.from_g2_projective(tmp).eq(
                G2Affine(
                    Fp2(
                        Fp(
                            [
                                0xE9D9_E2DA_9620_F98B,
                                0x54F1_1993_46B9_7F36,
                                0x3DB3_B820_376B_ED27,
                                0xCFDB_31C9_B0B6_4F4C,
                                0x41D7_C127_8635_4493,
                                0x0571_0794_C255_C064,
                            ]
                        ),
                        Fp(
                            [
                                0xD6C1_D3CA_6EA0_D06E,
                                0xDA0C_BD90_5595_489F,
                                0x4F53_52D4_3479_221D,
                                0x8ADE_5D73_6F8C_97E0,
                                0x48CC_8433_925E_F70E,
                                0x08D7_EA71_EA91_EF81,
                            ]
                        ),
                    ),
                    Fp2(
                        Fp(
                            [
                                0x15BA_26EB_4B0D_186F,
                                0x0D08_6D64_B7E9_E01E,
                                0xC8B8_48DD_652F_4C78,
                                0xEECF_46A6_123B_AE4F,
                                0x255E_8DD8_B6DC_812A,
                                0x1641_42AF_21DC_F93F,
                            ]
                        ),
                        Fp(
                            [
                                0xF9B4_A1A8_9598_4DB4,
                                0xD417_B114_CCCF_F748,
                                0x6856_301F_C89F_086E,
                                0x41C7_7787_8931_E3DA,
                                0x3556_B155_066A_2105,
                                0x00AC_F7D3_25CB_89CF,
                            ]
                        ),
                    ),
                    Choice(0),
                )
            )
        )


class TestAddition(unittest.TestCase):
    def test_projective_addition(self):
        a = G2Projective.identity()
        b = G2Projective.identity()
        c = a + b
        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

        a = G2Projective.identity()
        b = G2Projective.generator()
        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )
        b = G2Projective(
            b.x * z,
            b.y * z,
            z,
        )
        c = a + b
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())

        a = G2Projective.identity()
        b = G2Projective.generator()
        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )
        b = G2Projective(
            b.x * z,
            b.y * z,
            z,
        )
        c = b + a
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G2Projective.generator()))

        a = G2Projective.generator().double().double()  # 4P
        b = G2Projective.generator().double()  # 2P
        c = a + b
        d = G2Projective.generator()
        for _ in range(5):
            d += G2Projective.generator()
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

        beta = Fp2(
            Fp(
                [
                    0xCD03_C9E4_8671_F071,
                    0x5DAB_2246_1FCD_A5D2,
                    0x5870_42AF_D385_1B95,
                    0x8EB6_0EBE_01BA_CB9E,
                    0x03F9_7D6E_83D0_50D2,
                    0x18F0_2065_5463_8741,
                ]
            ),
            Fp.zero(),
        )
        beta = beta.square()
        a = G2Projective.generator().double().double()  # 4P
        b = G2Projective(
            a.x * beta,
            -a.y,
            a.z,
        )
        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())
        c = a + b
        self.assertTrue(
            G2Affine.from_g2_projective(c).eq(
                G2Affine.from_g2_projective(
                    G2Projective(
                        Fp2(
                            Fp(
                                [
                                    0x705A_BC79_9CA7_73D3,
                                    0xFE13_2292_C1D4_BF08,
                                    0xF37E_CE3E_07B2_B466,
                                    0x887E_1C43_F447_E301,
                                    0x1E09_70D0_33BC_77E8,
                                    0x1985_C81E_20A6_93F2,
                                ]
                            ),
                            Fp(
                                [
                                    0x1D79_B25D_B36A_B924,
                                    0x2394_8E4D_5296_39D3,
                                    0x471B_A7FB_0D00_6297,
                                    0x2C36_D4B4_465D_C4C0,
                                    0x82BB_C3CF_EC67_F538,
                                    0x051D_2728_B67B_F952,
                                ]
                            ),
                        ),
                        Fp2(
                            Fp(
                                [
                                    0x41B1_BBF6_576C_0ABF,
                                    0xB6CC_9371_3F7A_0F9A,
                                    0x6B65_B43E_48F3_F01F,
                                    0xFB7A_4CFC_AF81_BE4F,
                                    0x3E32_DADC_6EC2_2CB6,
                                    0x0BB0_FC49_D798_07E3,
                                ]
                            ),
                            Fp(
                                [
                                    0x7D13_9778_8F5F_2DDF,
                                    0xAB29_0714_4FF0_D8E8,
                                    0x5B75_73E0_CDB9_1F92,
                                    0x4CB8_932D_D31D_AF28,
                                    0x62BB_FAC6_DB05_2A54,
                                    0x11F9_5C16_D14C_3BBE,
                                ]
                            ),
                        ),
                        Fp2.one(),
                    )
                )
            )
        )
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())

    def test_mixed_addition(self):
        a = G2Affine.identity()
        b = G2Projective.identity()
        c = a + b
        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

        a = G2Affine.identity()
        b = G2Projective.generator()
        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )
        b = G2Projective(
            b.x * z,
            b.y * z,
            z,
        )
        c = a + b
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G2Projective.generator()))

        a = G2Affine.identity()
        b = G2Projective.generator()
        z = Fp2(
            Fp(
                [
                    0xBA7A_FA1F_9A6F_E250,
                    0xFA0F_5B59_5EAF_E731,
                    0x3BDC_4776_94C3_06E7,
                    0x2149_BE4B_3949_FA24,
                    0x64AA_6E06_49B2_078C,
                    0x12B1_08AC_3364_3C3E,
                ]
            ),
            Fp(
                [
                    0x1253_25DF_3D35_B5A8,
                    0xDC46_9EF5_555D_7FE3,
                    0x02D7_16D2_4431_06A9,
                    0x05A1_DB59_A6FF_37D0,
                    0x7CF7_784E_5300_BB8F,
                    0x16A8_8922_C7A5_E844,
                ]
            ),
        )
        b = G2Projective(
            b.x * z,
            b.y * z,
            z,
        )
        c = b + a
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G2Projective.generator()))

        a = G2Projective.generator().double().double()  # 4P
        b = G2Projective.generator().double()  # 2P
        c = a + b
        d = G2Projective.generator()
        for _ in range(5):
            d += G2Affine.generator()
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

        beta = Fp2(
            Fp(
                [
                    0xCD03_C9E4_8671_F071,
                    0x5DAB_2246_1FCD_A5D2,
                    0x5870_42AF_D385_1B95,
                    0x8EB6_0EBE_01BA_CB9E,
                    0x03F9_7D6E_83D0_50D2,
                    0x18F0_2065_5463_8741,
                ]
            ),
            Fp.zero(),
        )
        beta = beta.square()
        a = G2Projective.generator().double().double()  # 4P
        b = G2Projective(
            a.x * beta,
            -a.y,
            a.z,
        )
        a = G2Affine.from_g2_projective(a)
        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())
        c = a + b
        self.assertTrue(
            G2Affine.from_g2_projective(c).eq(
                G2Affine.from_g2_projective(
                    G2Projective(
                        Fp2(
                            Fp(
                                [
                                    0x705A_BC79_9CA7_73D3,
                                    0xFE13_2292_C1D4_BF08,
                                    0xF37E_CE3E_07B2_B466,
                                    0x887E_1C43_F447_E301,
                                    0x1E09_70D0_33BC_77E8,
                                    0x1985_C81E_20A6_93F2,
                                ]
                            ),
                            Fp(
                                [
                                    0x1D79_B25D_B36A_B924,
                                    0x2394_8E4D_5296_39D3,
                                    0x471B_A7FB_0D00_6297,
                                    0x2C36_D4B4_465D_C4C0,
                                    0x82BB_C3CF_EC67_F538,
                                    0x051D_2728_B67B_F952,
                                ]
                            ),
                        ),
                        Fp2(
                            Fp(
                                [
                                    0x41B1_BBF6_576C_0ABF,
                                    0xB6CC_9371_3F7A_0F9A,
                                    0x6B65_B43E_48F3_F01F,
                                    0xFB7A_4CFC_AF81_BE4F,
                                    0x3E32_DADC_6EC2_2CB6,
                                    0x0BB0_FC49_D798_07E3,
                                ]
                            ),
                            Fp(
                                [
                                    0x7D13_9778_8F5F_2DDF,
                                    0xAB29_0714_4FF0_D8E8,
                                    0x5B75_73E0_CDB9_1F92,
                                    0x4CB8_932D_D31D_AF28,
                                    0x62BB_FAC6_DB05_2A54,
                                    0x11F9_5C16_D14C_3BBE,
                                ]
                            ),
                        ),
                        Fp2.one(),
                    )
                )
            )
        )
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())


class TestSubNeg(unittest.TestCase):
    def test_projective_negation_and_subtraction(self):
        a = G2Projective.generator().double()
        self.assertTrue((a + (-a)).eq(G2Projective.identity()))
        self.assertTrue((a + (-a)).eq(a - a))


class TestScalarMultiplication(unittest.TestCase):
    def test_projective_scalar_multiplication(self):
        g = G2Projective.generator()
        a = Scalar(
            [
                0x2B56_8297_A56D_A71C,
                0xD8C3_9ECB_0EF3_75D1,
                0x435C_38DA_67BF_BF96,
                0x8088_A050_26B6_59B2,
            ]
        )
        b = Scalar(
            [
                0x785F_DD9B_26EF_8B85,
                0xC997_F258_3769_5C18,
                0x4C8D_BC39_E7B7_56C1,
                0x70D9_B6CC_6D87_DF20,
            ]
        )
        c = a * b
        self.assertTrue(((g * a) * b).eq(g * c))


class TestMultiplyByX(unittest.TestCase):
    def test_mul_by_x(self):
        # multiplying by `x` a point in G1 is the same as multiplying by
        # the equivalent scalar.
        generator = G2Projective.generator()
        x = -Scalar.from_u64(BLS_X) if (BLS_X_IS_NEGATIVE) else Scalar.from_u64(BLS_X)

        self.assertTrue(generator.mul_by_x().eq(generator * x))

        point = G2Projective.generator() * Scalar.from_u64(42)
        self.assertTrue(point.mul_by_x().eq(point * x))
