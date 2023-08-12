from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64
from src.fp import Fp


class Fp2:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

    @staticmethod
    def zero():
        return Fp2(Fp.zero(), Fp.zero())

    @staticmethod
    def default():
        return Fp2.zero()
