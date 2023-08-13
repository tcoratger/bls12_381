from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64
from src.fp import Fp


class Fp2:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

    @staticmethod
    def zero():
        return Fp2(Fp.zero(), Fp.zero())

    def is_zero(self):
        return self.c0.is_zero() and self.c1.is_zero()

    @staticmethod
    def default():
        return Fp2.zero()

    def conjugate(self):
        return Fp2(self.c0, -self.c1)

    def mul_by_nonresidue(self):
        # Multiply a + bu by u + 1, getting
        # au + a + bu^2 + bu
        # and because u^2 = -1, we get
        # (a - b) + (a + b)u
        return Fp2(self.c0 - self.c1, self.c0 + self.c1)
