from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64, CtOption
from src.fp import Fp
from src.fp2 import Fp2
from src.fp6 import Fp6


# This represents an element $c_0 + c_1 w$ of $\mathbb{F}_{p^12} = \mathbb{F}_{p^6} / w^2 - v$.
class Fp12:
    def __init__(self, c0: Fp6, c1: Fp6):
        self.c0 = c0
        self.c1 = c1

    def from_fp(f: Fp):
        return Fp12(Fp6.from_fp(f), Fp6.zero())

    def from_fp2(f: Fp2):
        return Fp12(Fp6.from_fp2(f), Fp6.zero())

    def from_fp6(f: Fp6):
        return Fp12(f, Fp6.zero())

    def zero():
        return Fp12(Fp6.zero(), Fp6.zero())

    def is_zero(self):
        return self.c0.is_zero() and self.c1.is_zero()

    def one():
        return Fp12(Fp6.one(), Fp6.zero())

    def default():
        return Fp12.zero()

    def eq(self, other):
        return self.c0 == other.c0 and self.c1 == other.c1 and self.c2 == other.c2

    @staticmethod
    def random(rng):
        return Fp12(Fp6.random(rng), Fp6.random(rng))

    def mul_by_014(self, c0: Fp2, c1: Fp2, c4: Fp2):
        aa = self.c0.mul_by_01(c0, c1)
        bb = self.c1.mul_by_1(c4)
        o = c1 + c4
        c1 = self.c1 + self.c0
        c1 = c1.mul_by_01(c0, o)
        c1 = c1 - aa - bb
        c0 = bb
        c0 = c0.mul_by_nonresidue()
        c0 = c0 + aa

        Fp12(c0, c1)

    def conjugate(self):
        return Fp12(self.c0, -self.c1)
