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
        a = G2Affine.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp2.one()) and a.infinity)
        self.assertTrue(a.is_identity())

    def test_default(self):
        a = G2Affine.default()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp2.one()) and a.infinity)

    def test_affine_point_equality(self):
        a = G2Affine.generator()
        b = G2Affine.identity()
        self.assertTrue(a.eq(a))
        self.assertTrue(b.eq(b))
        self.assertFalse(a.eq(b))
        self.assertFalse(b.eq(a))


class TestConditionnalSelect(unittest.TestCase):
    def test_conditionally_select_affine(self):
        a = G2Affine.generator()
        b = G2Affine.identity()

        case0 = G2Affine.conditional_select(a, b, Choice(0))
        case1 = G2Affine.conditional_select(a, b, Choice(1))

        self.assertTrue(
            case0.x.eq(a.x)
            and case0.y.eq(a.y)
            and case0.infinity.value == a.infinity.value
        )
        self.assertTrue(
            case1.x.eq(b.x)
            and case1.y.eq(b.y)
            and case1.infinity.value == b.infinity.value
        )


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G2Affine.identity().is_on_curve())
        self.assertTrue(G2Affine.generator().is_on_curve())


class TestProjectiveToAffine(unittest.TestCase):
    def test_projective_to_affine(self):
        a = G2Projective.generator()
        b = G2Projective.identity()

        self.assertTrue(G2Affine.from_g2_projective(a).is_on_curve())
        self.assertFalse(G2Affine.from_g2_projective(a).is_identity())
        self.assertTrue(G2Affine.from_g2_projective(b).is_on_curve())
        self.assertTrue(G2Affine.from_g2_projective(b).is_identity())

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
        self.assertTrue(G2Affine.from_g2_projective(c).eq(G2Affine.generator()))


class TestSubNeg(unittest.TestCase):
    def test_affine_negation_and_subtraction(self):
        a = G2Affine.generator()

        self.assertTrue(
            (G2Projective.from_g2_affine(a) + (-a)).eq(G2Projective.identity())
        )
        self.assertTrue(
            (G2Projective.from_g2_affine(a) + (-a)).eq(
                G2Projective.from_g2_affine(a) - a
            )
        )


class TestScalarMultiplication(unittest.TestCase):
    def test_affine_scalar_multiplication(self):
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
        self.assertTrue((G2Affine.from_g2_projective(g * a) * b).eq(g * c))


class TestTorsionFree(unittest.TestCase):
    def test_is_torsion_free(self):
        a = G2Affine(
            Fp2(
                Fp(
                    [
                        0x89F5_50C8_13DB_6431,
                        0xA50B_E8C4_56CD_8A1A,
                        0xA45B_3741_14CA_E851,
                        0xBB61_90F5_BF7F_FF63,
                        0x970C_A02C_3BA8_0BC7,
                        0x02B8_5D24_E840_FBAC,
                    ]
                ),
                Fp(
                    [
                        0x6888_BC53_D707_16DC,
                        0x3DEA_6B41_1768_2D70,
                        0xD8F5_F930_500C_A354,
                        0x6B5E_CB65_56F5_C155,
                        0xC96B_EF04_3477_8AB0,
                        0x0508_1505_5150_06AD,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x3CF1_EA0D_434B_0F40,
                        0x1A0D_C610_E603_E333,
                        0x7F89_9561_60C7_2FA0,
                        0x25EE_03DE_CF64_31C5,
                        0xEEE8_E206_EC0F_E137,
                        0x0975_92B2_26DF_EF28,
                    ]
                ),
                Fp(
                    [
                        0x71E8_BB5F_2924_7367,
                        0xA5FE_049E_2118_31CE,
                        0x0CE6_B354_502A_3896,
                        0x93B0_1200_0997_314E,
                        0x6759_F3B6_AA5B_42AC,
                        0x1569_44C4_DFE9_2BBB,
                    ]
                ),
            ),
            Choice(0),
        )
        self.assertFalse(a.is_torsion_free())
        self.assertTrue(G2Affine.identity().is_torsion_free())
        self.assertTrue(G2Affine.generator().is_torsion_free())
