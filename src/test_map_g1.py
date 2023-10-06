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

from src.map_g1 import sng0, P_M1_OVER2


class TestSignO(unittest.TestCase):
    def test_sgn0(self):
        self.assertTrue(sng0(Fp.zero()).value == 0)
        self.assertTrue(sng0(Fp.one()).value == 1)
        self.assertTrue(sng0(-Fp.one()).value == 0)
        self.assertTrue(sng0(-Fp.zero()).value == 0)
        self.assertTrue(sng0(P_M1_OVER2).value == 1)
        self.assertTrue(sng0(P_M1_OVER2 + Fp.one()).value == 0)
