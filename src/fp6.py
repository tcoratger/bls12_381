from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64, CtOption
from src.fp import Fp
from src.fp2 import Fp2


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
