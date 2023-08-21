from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64, CtOption
from src.fp import Fp
from src.fp2 import Fp2


# This represents an element $c_0 + c_1 v + c_2 v^2$ of $\mathbb{F}_{p^6} = \mathbb{F}_{p^2} / v^3 - u - 1$.
class Fp6:
    def __init__(self, c0: Fp2, c1: Fp2, c2: Fp2):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def from_fp(f: Fp):
        return Fp6(Fp2.from_fp(f), Fp2.zero(), Fp2.zero())

    def from_fp2(f: Fp2):
        return Fp6(f, Fp2.zero(), Fp2.zero())

    def eq(self, other):
        return self.c0.eq(other.c0) and self.c1.eq(other.c1) and self.c2.eq(other.c2)

    def zero():
        return Fp6(Fp2.zero(), Fp2.zero(), Fp2.zero())

    def one():
        return Fp6(Fp2.one(), Fp2.zero(), Fp2.zero())

    def default():
        return Fp6.zero()

    @staticmethod
    def random(rng):
        return Fp6(Fp2.random(rng), Fp2.random(rng), Fp2.random(rng))

    def mul_by_1(self, c1: Fp2):
        return Fp6((self.c2 * c1).mul_by_nonresidue(), self.c0 * c1, self.c1 * c1)

    def mul_by_01(self, c0: Fp2, c1: Fp2):
        a_a = self.c0 * c0
        b_b = self.c1 * c1
        t1 = (self.c2 * c1).mul_by_nonresidue() + a_a
        t2 = (c0 + c1) * (self.c0 + self.c1) - a_a - b_b
        t3 = self.c2 * c0 + b_b
        return Fp6(t1, t2, t3)

    # Multiply by quadratic nonresidue v.
    def mul_by_nonresidue(self):
        # Given a + bv + cv^2, this produces
        #     av + bv^2 + cv^3
        # but because v^3 = u + 1, we have
        #     c(u + 1) + av + v^2

        return Fp6(self.c2.mul_by_nonresidue(), self.c0, self.c1)
