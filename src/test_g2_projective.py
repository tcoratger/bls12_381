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
from src.utils import array_to_number, Choice
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
