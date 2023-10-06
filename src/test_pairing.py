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
from src.pairing import (
    MillerLoopResult,
    Gt,
    pairing,
    ell,
    G2Prepared,
    multi_miller_loop,
)


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


class TestUnitary(unittest.TestCase):
    def test_unitary(self):
        g = G1Affine.generator()
        h = G2Affine.generator()

        p = -pairing(g, h)
        q = pairing(g, -h)
        r = pairing(-g, h)

        self.assertTrue(p.eq(q))
        self.assertTrue(q.eq(r))


class TestMultiMillerLoop(unittest.TestCase):
    def test_multi_miller_loop(self):
        a1 = G1Affine.generator()
        b1 = G2Affine.generator()

        a2 = G1Affine.from_g1_projective(
            G1Affine.generator() * Scalar.from_raw([1, 2, 3, 4]).invert().value.square()
        )
        b2 = G2Affine.from_g2_projective(
            G2Affine.generator() * Scalar.from_raw([4, 2, 2, 4]).invert().value.square()
        )

        a3 = G1Affine.identity()
        b3 = G2Affine.from_g2_projective(
            G2Affine.generator() * Scalar.from_raw([9, 2, 2, 4]).invert().value.square()
        )

        a4 = G1Affine.from_g1_projective(
            G1Affine.generator() * Scalar.from_raw([5, 5, 5, 5]).invert().value.square()
        )
        b4 = G2Affine.identity()

        a5 = G1Affine.from_g1_projective(
            G1Affine.generator()
            * Scalar.from_raw([323, 32, 3, 1]).invert().value.square(),
        )
        b5 = G2Affine.from_g2_projective(
            G2Affine.generator()
            * Scalar.from_raw([4, 2, 2, 9099]).invert().value.square(),
        )

        b1_prepared = G2Prepared.from_g2_affine(b1)
        b2_prepared = G2Prepared.from_g2_affine(b2)
        b3_prepared = G2Prepared.from_g2_affine(b3)
        b4_prepared = G2Prepared.from_g2_affine(b4)
        b5_prepared = G2Prepared.from_g2_affine(b5)

        expected = (
            pairing(a1, b1)
            + pairing(a2, b2)
            + pairing(a3, b3)
            + pairing(a4, b4)
            + pairing(a5, b5)
        )

        test = multi_miller_loop(
            [
                (a1, b1_prepared),
                (a2, b2_prepared),
                (a3, b3_prepared),
                (a4, b4_prepared),
                (a5, b5_prepared),
            ]
        ).final_exponentiation()

        self.assertTrue(expected.eq(test))

    def tricking_miller_loop_result(self):
        self.assertTrue(
            multi_miller_loop(
                [G1Affine.identity(), G2Prepared.from_g2_affine(G2Affine.generator())]
            ).fp.eq(Fp12.one())
        )
        self.assertTrue(
            multi_miller_loop(
                [G1Affine.generator(), G2Prepared.from_g2_affine(G2Affine.identity())]
            ).fp.eq(Fp12.one())
        )
        self.assertFalse(
            multi_miller_loop(
                [
                    (
                        G1Affine.generator(),
                        G2Prepared.from_g2_affine(G2Affine.generator()),
                    ),
                    (
                        -G1Affine.generator(),
                        G2Prepared.from_g2_affine(G2Affine.generator()),
                    ),
                ]
            )
            .final_exponentiation()
            .eq(Gt.identity())
        )
