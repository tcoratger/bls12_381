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
from src.pairing import MillerLoopResult, Gt, pairing, ell


class TestMillerLoopResult(unittest.TestCase):
    def test_default(self):
        self.assertTrue(MillerLoopResult.default().fp.eq(Fp12.one()))

    def test_miller_loop_result_default(self):
        self.assertTrue(
            MillerLoopResult.default().final_exponentiation().eq(Gt.identity())
        )


class TestGt(unittest.TestCase):
    def test_default(self):
        self.assertTrue(Gt.identity().fp.eq(Fp12.one()))
        self.assertTrue(Gt.default().fp.eq(Fp12.one()))
        self.assertTrue(Gt.default().eq(Gt.identity()))

    def test_gt_generator(self):
        self.assertTrue(
            Gt.generator().eq(pairing(G1Affine.generator(), G2Affine.generator()))
        )

    def test_bilinearity(self):
        a = Scalar.from_raw([1, 2, 3, 4]).invert().value.square()
        b = Scalar.from_raw([5, 6, 7, 8]).invert().value.square()
        c = a * b

        g = G1Affine.from_g1_projective(G1Affine.generator() * a)
        h = G2Affine.from_g2_projective(G2Affine.generator() * b)
        p = pairing(g, h)

        self.assertFalse(p.eq(Gt.identity()))

        expected = G1Affine.from_g1_projective(G1Affine.generator() * c)
        self.assertTrue(p.eq(pairing(expected, G2Affine.generator())))
        self.assertTrue(p.eq(pairing(G1Affine.generator(), G2Affine.generator()) * c))
