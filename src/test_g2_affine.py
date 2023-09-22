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
from src.g2 import G2Affine
import random
from src.utils import array_to_number, Choice
from src.scalar import Scalar


class TestG2(unittest.TestCase):
    def test_identity(self):
        a = G2Affine.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp2.one()) and a.infinity.value == 1)
        self.assertTrue(a.is_identity().value == 1)

    def test_default(self):
        a = G2Affine.default()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp2.one()) and a.infinity.value == 1)

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
