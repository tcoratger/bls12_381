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
from src.g1 import G1Affine, G1Projective
import random
from src.utils import array_to_number, Choice


class TestG1(unittest.TestCase):
    def test_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp.one()) and a.z.is_zero())

    def test_is_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.is_identity())


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G1Projective.identity().is_on_curve())
        self.assertTrue(G1Projective.generator().is_on_curve())
