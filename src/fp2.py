from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64
from src.fp import Fp


class Fp2:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

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

    def sub(self, rhs):
        return Fp2(self.c0 - rhs.c0, self.c1 - rhs.c1)

    def add(self, rhs):
        return Fp2(self.c0 + rhs.c0, self.c1 + rhs.c1)

    def mul(self, rhs):
        # F_{p^2} x F_{p^2} multiplication implemented with operand scanning (schoolbook)
        # computes the result as:

        #  a·b = (a_0 b_0 + a_1 b_1 β) + (a_0 b_1 + a_1 b_0)i

        #  In BLS12-381's F_{p^2}, our β is -1, so the resulting F_{p^2} element is:

        #    c_0 = a_0 b_0 - a_1 b_1
        #    c_1 = a_0 b_1 + a_1 b_0

        #  Each of these is a "sum of products", which we can compute efficiently.

        return Fp2(
            Fp.sum_of_products([self.c0, -self.c1], [rhs.c0, rhs.c1]),
            Fp.sum_of_products([self.c0, self.c1], [rhs.c1, rhs.c0]),
        )

    def square(self):
        # Complex squaring:

        #  v0  = c0 * c1
        #  c0' = (c0 + c1) * (c0 + \beta*c1) - v0 - \beta * v0
        #  c1' = 2 * v0

        #  In BLS12-381's F_{p^2}, our \beta is -1 so we
        #  can modify this formula:

        #  c0' = (c0 + c1) * (c0 - c1)
        #  c1' = 2 * c0 * c1

        a = self.c0 + self.c1
        b = self.c0 - self.c1
        c = self.c0 + self.c0

        return Fp2(a * b, c * self.c1)

    @staticmethod
    def random(rng):
        return Fp2(Fp.random(rng), Fp.random(rng))

    # Raises this element to p.
    def frobenius_map(self):
        # This is always just a conjugation.
        return self.conjugate()
