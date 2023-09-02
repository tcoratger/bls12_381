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
import random
from src.utils import array_to_number, Choice, BLS_X, BLS_X_IS_NEGATIVE
from src.scalar import Scalar


class TestG1(unittest.TestCase):
    def test_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp.one()) and a.z.is_zero())

    def test_is_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.is_identity())


class TestBeta(unittest.TestCase):
    def test_beta(self):
        self.assertTrue(
            BETA.eq(
                Fp.from_bytes(
                    [
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x5F,
                        0x19,
                        0x67,
                        0x2F,
                        0xDF,
                        0x76,
                        0xCE,
                        0x51,
                        0xBA,
                        0x69,
                        0xC6,
                        0x07,
                        0x6A,
                        0x0F,
                        0x77,
                        0xEA,
                        0xDD,
                        0xB3,
                        0xA9,
                        0x3B,
                        0xE6,
                        0xF8,
                        0x96,
                        0x88,
                        0xDE,
                        0x17,
                        0xD8,
                        0x13,
                        0x62,
                        0x0A,
                        0x00,
                        0x02,
                        0x2E,
                        0x01,
                        0xFF,
                        0xFF,
                        0xFF,
                        0xFE,
                        0xFF,
                        0xFE,
                    ]
                ).value
            )
        )
        self.assertFalse(BETA.eq(Fp.one()))
        self.assertFalse((BETA * BETA).eq(Fp.one()))
        self.assertTrue((BETA * BETA * BETA).eq(Fp.one()))


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G1Projective.identity().is_on_curve())
        self.assertTrue(G1Projective.generator().is_on_curve())

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        gen = G1Affine.generator()
        test = G1Projective(gen.x * z, gen.y * z, z)
        self.assertTrue(test.is_on_curve())
        test.x = z
        self.assertFalse(test.is_on_curve())


class TestEquality(unittest.TestCase):
    def test_projective_point_equality(self):
        a = G1Projective.generator()
        b = G1Projective.identity()

        self.assertTrue(a.eq(a))
        self.assertTrue(b.eq(b))
        self.assertFalse(a.eq(b))
        self.assertFalse(b.eq(a))

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        c = G1Projective(
            a.x * z,
            a.y * z,
            z,
        )

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


class TestFromAffine(unittest.TestCase):
    def test_affine_to_projective(self):
        a = G1Affine.generator()
        b = G1Affine.identity()

        self.assertTrue(G1Projective.from_g1_affine(a).is_on_curve())
        self.assertFalse(G1Projective.from_g1_affine(a).is_identity())
        self.assertTrue(G1Projective.from_g1_affine(b).is_on_curve())
        self.assertTrue(G1Projective.from_g1_affine(b).is_identity())


class TestConditionallySelect(unittest.TestCase):
    def test_conditionally_select_projective(self):
        a = G1Projective.generator()
        b = G1Projective.identity()

        self.assertTrue(G1Projective.conditional_select(a, b, Choice(0)).eq(a))
        self.assertTrue(G1Projective.conditional_select(a, b, Choice(1)).eq(b))


class TestProjectiveAddition(unittest.TestCase):
    def test_projective_addition1(self):
        a = G1Projective.identity()
        b = G1Projective.identity()

        c = a + b

        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

    def test_projective_addition2(self):
        a = G1Projective.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = a + b
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_projective_addition3(self):
        a = G1Projective.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = b + a

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_projective_addition4(self):
        a = G1Projective.generator().double().double()  # 4P
        b = G1Projective.generator().double()  # 2P

        c = a + b

        d = G1Projective.generator()

        for _ in range(5):
            d += G1Projective.generator()

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

    def test_projective_addition_degenerate(self):
        beta = Fp(
            [
                0xCD03_C9E4_8671_F071,
                0x5DAB_2246_1FCD_A5D2,
                0x5870_42AF_D385_1B95,
                0x8EB6_0EBE_01BA_CB9E,
                0x03F9_7D6E_83D0_50D2,
                0x18F0_2065_5463_8741,
            ]
        )
        beta = beta.square()
        a = G1Projective.generator().double().double()
        b = G1Projective(a.x * beta, -a.y, a.z)

        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())

        c = a + b

        self.assertTrue(
            G1Affine.from_g1_projective(c).eq(
                G1Affine.from_g1_projective(
                    G1Projective(
                        Fp(
                            [
                                0x29E1_E987_EF68_F2D0,
                                0xC5F3_EC53_1DB0_3233,
                                0xACD6_C4B6_CA19_730F,
                                0x18AD_9E82_7BC2_BAB7,
                                0x46E3_B2C5_785C_C7A9,
                                0x07E5_71D4_2D22_DDD6,
                            ]
                        ),
                        Fp(
                            [
                                0x94D1_17A7_E5A5_39E7,
                                0x8E17_EF67_3D4B_5D22,
                                0x9D74_6AAF_508A_33EA,
                                0x8C6D_883D_2516_C9A2,
                                0x0BC3_B8D5_FB04_47F7,
                                0x07BF_A4C7_210F_4F44,
                            ]
                        ),
                        Fp.one(),
                    )
                )
            )
        )

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())


class TestMixedAddition(unittest.TestCase):
    def test_mixed_addition1(self):
        a = G1Affine.identity()
        b = G1Projective.identity()

        c = a + b

        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

    def test_mixed_addition2(self):
        a = G1Affine.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = a + b

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_mixed_addition3(self):
        a = G1Affine.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = b + a

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_mixed_addition4(self):
        a = G1Projective.generator().double().double()  # 4P
        b = G1Projective.generator().double()  # 2P

        c = a + b

        d = G1Projective.generator()

        for _ in range(5):
            d += G1Projective.generator()

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

    def test_projective_addition_degenerate(self):
        beta = Fp(
            [
                0xCD03_C9E4_8671_F071,
                0x5DAB_2246_1FCD_A5D2,
                0x5870_42AF_D385_1B95,
                0x8EB6_0EBE_01BA_CB9E,
                0x03F9_7D6E_83D0_50D2,
                0x18F0_2065_5463_8741,
            ]
        )
        beta = beta.square()
        a = G1Projective.generator().double().double()
        b = G1Projective(a.x * beta, -a.y, a.z)

        a = G1Affine.from_g1_projective(a)

        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())

        c = a + b

        self.assertTrue(
            G1Affine.from_g1_projective(c).eq(
                G1Affine.from_g1_projective(
                    G1Projective(
                        Fp(
                            [
                                0x29E1_E987_EF68_F2D0,
                                0xC5F3_EC53_1DB0_3233,
                                0xACD6_C4B6_CA19_730F,
                                0x18AD_9E82_7BC2_BAB7,
                                0x46E3_B2C5_785C_C7A9,
                                0x07E5_71D4_2D22_DDD6,
                            ]
                        ),
                        Fp(
                            [
                                0x94D1_17A7_E5A5_39E7,
                                0x8E17_EF67_3D4B_5D22,
                                0x9D74_6AAF_508A_33EA,
                                0x8C6D_883D_2516_C9A2,
                                0x0BC3_B8D5_FB04_47F7,
                                0x07BF_A4C7_210F_4F44,
                            ]
                        ),
                        Fp.one(),
                    )
                )
            )
        )

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())


class TestDoubling(unittest.TestCase):
    def test_doubling1(self):
        tmp = G1Projective.identity().double()

        self.assertTrue(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

    def test_doubling2(self):
        tmp = G1Projective.generator().double()

        self.assertFalse(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

        self.assertTrue(
            G1Affine.from_g1_projective(tmp).eq(
                G1Affine(
                    Fp(
                        [
                            0x53E9_78CE_58A9_BA3C,
                            0x3EA0_583C_4F3D_65F9,
                            0x4D20_BB47_F001_2960,
                            0xA54C_664A_E5B2_B5D9,
                            0x26B5_52A3_9D7E_B21F,
                            0x0008_895D_26E6_8785,
                        ]
                    ),
                    Fp(
                        [
                            0x7011_0B32_9829_3940,
                            0xDA33_C539_3F1F_6AFC,
                            0xB86E_DFD1_6A5A_A785,
                            0xAEC6_D1C9_E7B1_C895,
                            0x25CF_C2B5_22D1_1720,
                            0x0636_1C83_F8D0_9B15,
                        ]
                    ),
                    Choice(0),
                )
            )
        )


class TestNegSub(unittest.TestCase):
    def test_projective_negation_and_subtraction(self):
        a = G1Projective.generator().double()

        self.assertTrue((a + (-a)).is_identity())
        self.assertTrue((a + (-a)).eq(G1Projective.identity()))


class TestScalarMultiplication(unittest.TestCase):
    def test_projective_scalar_multiplication(self):
        g = G1Projective.generator()
        a = Scalar.from_raw(
            [
                0x2B56_8297_A56D_A71C,
                0xD8C3_9ECB_0EF3_75D1,
                0x435C_38DA_67BF_BF96,
                0x8088_A050_26B6_59B2,
            ]
        )
        b = Scalar.from_raw(
            [
                0x785F_DD9B_26EF_8B85,
                0xC997_F258_3769_5C18,
                0x4C8D_BC39_E7B7_56C1,
                0x70D9_B6CC_6D87_DF20,
            ]
        )
        c = a * b
        self.assertTrue(((g * a) * b).eq(g * c))


class TestMulByX(unittest.TestCase):
    def test_mul_by_x(self):
        # multiplying by `x` a point in G1 is the same as multiplying by
        # the equivalent scalar.
        generator = G1Projective.generator()
        x = -Scalar.from_u64(BLS_X) if (BLS_X_IS_NEGATIVE) else Scalar.from_u64(BLS_X)

        self.assertTrue(generator.mul_by_x().eq(generator * x))

        point = G1Projective.generator() * Scalar.from_u64(42)
        self.assertTrue(point.mul_by_x().eq(point * x))


class TestClearCoFactor(unittest.TestCase):
    def test_clear_cofactor(self):
        generator = G1Projective.generator()
        self.assertTrue(generator.clear_cofactor().is_on_curve())

        id = G1Projective.identity()
        self.assertTrue(id.clear_cofactor().is_on_curve())

        z = Fp(
            [
                0x3D2D1C670671394E,
                0x0EE3A800A2F7C1CA,
                0x270F4F21DA2E5050,
                0xE02840A53F1BE768,
                0x55DEBEB597512690,
                0x08BD25353DC8F791,
            ]
        )

        point = G1Projective(
            Fp(
                [
                    0x48AF5FF540C817F0,
                    0xD73893ACAF379D5A,
                    0xE6C43584E18E023C,
                    0x1EDA39C30F188B3E,
                    0xF618C6D3CCC0F8D8,
                    0x0073542CD671E16C,
                ]
            )
            * z,
            Fp(
                [
                    0x57BF8BE79461D0BA,
                    0xFC61459CEE3547C3,
                    0x0D23567DF1EF147B,
                    0x0EE187BCCE1D9B64,
                    0xB0C8CFBE9DC8FDC1,
                    0x1328661767EF368B,
                ]
            ),
            z.square() * z,
        )

        self.assertTrue(point.is_on_curve())
        self.assertFalse(G1Affine.from_g1_projective(point).is_torsion_free())

        cleared_point = point.clear_cofactor()
        self.assertTrue(cleared_point.is_on_curve())
        self.assertTrue(G1Affine.from_g1_projective(cleared_point).is_torsion_free())

        # in BLS12-381 the cofactor in G1 can be
        # cleared multiplying by (1-x)
        h_eff = Scalar.from_u64(1) + Scalar.from_u64(BLS_X)
        self.assertTrue(point.clear_cofactor().eq(point * h_eff))


class TestBatchNormalize(unittest.TestCase):
    def test_batch_normalize(self):
        a = G1Projective.generator().double()
        b = a.double()
        c = b.double()

        for a_identity in [False, True]:
            for b_identity in [False, True]:
                for c_identity in [False, True]:
                    v = [a, b, c]
                    if a_identity:
                        v[0] = G1Projective.identity()
                    if b_identity:
                        v[1] = G1Projective.identity()
                    if c_identity:
                        v[2] = G1Projective.identity()

                    t = [G1Affine.identity(), G1Affine.identity(), G1Affine.identity()]
                    expected = [
                        G1Affine.from_g1_projective(v[0]),
                        G1Affine.from_g1_projective(v[1]),
                        G1Affine.from_g1_projective(v[2]),
                    ]

                    G1Projective.batch_normalize(v, t)

                    for i in range(3):
                        self.assertTrue(t[i].eq(expected[i]))
