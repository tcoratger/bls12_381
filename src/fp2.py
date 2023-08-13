from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64
from src.fp import Fp


class Fp2:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

    def __neg__(self):
        return self.neg()

    @staticmethod
    def zero():
        return Fp2(Fp.zero(), Fp.zero())

    @staticmethod
    def one():
        return Fp2(Fp.one(), Fp.zero())

    def eq(self, other):
        return self.c0.eq(other.c0) and self.c1.eq(other.c1)

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

    # Returns whether or not this element is strictly lexicographically
    # larger than its negation.
    def lexicographically_largest(self):
        # If this element's c1 coefficient is lexicographically largest
        # then it is lexicographically largest. Otherwise, in the event
        # the c1 coefficient is zero and the c0 coefficient is
        # lexicographically largest, then this element is lexicographically
        # largest.
        return self.c1.lexicographically_largest() or (
            self.c1.is_zero() and self.c0.lexicographically_largest()
        )

    def neg(self):
        return Fp2(-self.c0, -self.c1)
