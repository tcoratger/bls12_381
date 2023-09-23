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
