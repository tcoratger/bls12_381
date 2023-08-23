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
