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


if __name__ == "__main__":
    unittest.main()
