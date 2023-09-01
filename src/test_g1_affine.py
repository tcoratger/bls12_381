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
from src.utils import array_to_number, Choice
from src.scalar import Scalar


class TestG1(unittest.TestCase):
    def test_identity(self):
        a = G1Affine.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp.one()) and a.infinity.value == 1)

    def test_is_identity(self):
        a = G1Affine.identity()
        self.assertTrue(a.is_identity())

    def test_default(self):
        a = G1Affine.default()
        self.assertTrue(a.eq(G1Affine.identity()))


class TestConditionnalSelect(unittest.TestCase):
    def test_conditional_select(self):
        a = Fp(
            [
                0xDC90_6D9B_E3F9_5DC8,
                0x8755_CAF7_4596_91A1,
                0xCFF1_A7F4_E958_3AB3,
                0x9B43_821F_849E_2284,
                0xF575_54F3_A297_4F3F,
                0x085D_BEA8_4ED4_7F79,
            ]
        )
        b = Fp(
            [
                0xA1FA_FFFF_FFFE_5557,
                0x995B_FFF9_76A3_FFFE,
                0x03F4_1D24_D174_CEB4,
                0xF654_7998_C199_5DBD,
                0x778A_468F_507A_6034,
                0x0205_5993_1F7F_8103,
            ]
        )

        c = G1Affine(a, b, Choice(1))
        d = G1Affine(b, a, Choice(0))

        case0 = G1Affine.conditional_select(c, d, Choice(0))
        case1 = G1Affine.conditional_select(c, d, Choice(1))

        self.assertTrue(
            case0.x.eq(c.x) and case0.y.eq(c.y) and case0.infinity.value == 1
        )
        self.assertTrue(
            case1.x.eq(d.x) and case1.y.eq(d.y) and case1.infinity.value == 0
        )


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G1Affine.identity().is_on_curve())
        self.assertTrue(G1Affine.generator().is_on_curve())


class TestBeta(unittest.TestCase):
    def test_beta(self):
        self.assertFalse(BETA.eq(Fp.one()))
        self.assertFalse((BETA * BETA).eq(Fp.one()))
        self.assertTrue((BETA * BETA * BETA).eq(Fp.one()))


class TestEquality(unittest.TestCase):
    def test_affine_point_equality(self):
        a = G1Affine.generator()
        b = G1Affine.identity()
        self.assertTrue(a.eq(a))
        self.assertTrue(b.eq(b))
        self.assertFalse(a.eq(b))
        self.assertFalse(b.eq(a))


class TestFromProjective(unittest.TestCase):
    def test_projective_to_affine(self):
        a = G1Projective.generator()
        b = G1Projective.identity()

        self.assertTrue(G1Affine.from_g1_projective(a).is_on_curve())
        self.assertTrue(G1Affine.from_g1_projective(a).is_identity())
        self.assertTrue(G1Affine.from_g1_projective(b).is_on_curve())
        self.assertTrue(G1Affine.from_g1_projective(b).is_on_curve())

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

        self.assertTrue(G1Affine.from_g1_projective(c).eq(G1Affine.generator()))


class TestConditionallySelect(unittest.TestCase):
    def test_conditionally_select_affine(self):
        a = G1Affine.generator()
        b = G1Affine.identity()

        self.assertTrue(G1Affine.conditional_select(a, b, Choice(0)).eq(a))
        self.assertTrue(G1Affine.conditional_select(a, b, Choice(1)).eq(b))


class TestNegSub(unittest.TestCase):
    def test_affine_negation_and_subtraction(self):
        a = G1Affine.generator()

        self.assertTrue((G1Projective.from_g1_affine(a) + (-a)).is_identity())
        self.assertTrue(
            (G1Projective.from_g1_affine(a) + (-a)).eq(
                G1Projective.from_g1_affine(a) - a
            )
        )


class TestScalarMultiplication(unittest.TestCase):
    def test_affine_scalar_multiplication(self):
        g = G1Affine.generator()
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
        self.assertTrue((G1Affine.from_g1_projective(g * a) * b).eq(g * c))


class TestTorsionFree(unittest.TestCase):
    def test_is_torsion_free(self):
        a = G1Affine(
            Fp(
                [
                    0x0ABA_F895_B97E_43C8,
                    0xBA4C_6432_EB9B_61B0,
                    0x1250_6F52_ADFE_307F,
                    0x7502_8C34_3933_6B72,
                    0x8474_4F05_B8E9_BD71,
                    0x113D_554F_B095_54F7,
                ]
            ),
            Fp(
                [
                    0x73E9_0E88_F5CF_01C0,
                    0x3700_7B65_DD31_97E2,
                    0x5CF9_A199_2F0D_7C78,
                    0x4F83_C10B_9EB3_330D,
                    0xF6A6_3F6F_07F6_0961,
                    0x0C53_B5B9_7E63_4DF3,
                ]
            ),
            Choice(0),
        )
        self.assertFalse(a.is_torsion_free())
        self.assertTrue(G1Affine.identity().is_torsion_free())
        self.assertTrue(G1Affine.generator().is_torsion_free())


if __name__ == "__main__":
    unittest.main()
