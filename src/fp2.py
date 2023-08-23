from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64, CtOption
from src.fp import Fp


class Fp2:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

    def __str__(self):
        # result = f"Fp2:\n"
        # result += f"c0: {self.c0}\n"
        # result += f"c1: {self.c1}\n"
        # return result
        # result = f"Fp2:\n"
        # result += f"c0: {self.c0}\n"
        result = f"({self.c0} + {self.c1} * u)\n"
        return result

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def from_fp(f: Fp):
        return Fp2(f, Fp.zero())

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

    # Computes the multiplicative inverse of this field
    # element, returning None in the case that this element
    # is zero.
    def invert(self):
        # We wish to find the multiplicative inverse of a nonzero
        # element a + bu in Fp2. We leverage an identity

        # (a + bu)(a - bu) = a^2 + b^2

        # which holds because u^2 = -1. This can be rewritten as

        # (a + bu)(a - bu)/(a^2 + b^2) = 1

        # because a^2 + b^2 = 0 has no nonzero solutions for (a, b).
        # This gives that (a - bu)/(a^2 + b^2) is the inverse
        # of (a + bu). Importantly, this can be computing using
        # only a single inversion in Fp.

        result = ((self.c0).square() + (self.c1).square()).invert()

        if result.choice:
            return CtOption(
                Fp2(self.c0 * result.value, self.c1 * (-result.value)), True
            )

        return CtOption(None, True)

    def pow_vartime(self, by):
        res = Fp2.one()

        for e in reversed(by):
            for i in reversed(range(64)):
                res = res.square()

                if (e >> i) & 1 == 1:
                    res *= self

        return res

    def sqrt(self):
        # Algorithm 9, https://eprint.iacr.org/2012/685.pdf
        # with constant time modifications.
        if self.is_zero():
            return CtOption(Fp2.zero(), True)

        # a1 = self^((p - 3) / 4)
        a1 = self.pow_vartime(
            [
                0xEE7F_BFFF_FFFF_EAAA,
                0x07AA_FFFF_AC54_FFFF,
                0xD9CC_34A8_3DAC_3D89,
                0xD91D_D2E1_3CE1_44AF,
                0x92C6_E9ED_90D2_EB35,
                0x0680_447A_8E5F_F9A6,
            ]
        )

        # alpha = a1^2 * self = self^((p - 3) / 2 + 1) = self^((p - 1) / 2)
        alpha = a1.square() * self
        # x0 = self^((p + 1) / 4)
        x0 = a1 * self

        # In the event that alpha = -1, the element is order p - 1 and so
        # we're just trying to get the square of an element of the subfield
        # Fp. This is given by x0 * u, since u = sqrt(-1). Since the element
        # x0 = a + bu has b = 0, the solution is therefore au.
        if alpha.eq(-Fp2.one()):
            return CtOption(Fp2(-x0.c1, x0.c0), alpha.eq(-Fp2.one()))

        # Otherwise, the correct solution is (1 + alpha)^((q - 1) // 2) * x0
        result = (alpha + Fp2.one()).pow_vartime(
            [
                0xDCFF_7FFF_FFFF_D555,
                0x0F55_FFFF_58A9_FFFF,
                0xB398_6950_7B58_7B12,
                0xB23B_A5C2_79C2_895F,
                0x258D_D3DB_21A5_D66B,
                0x0D00_88F5_1CBF_F34D,
            ]
        ) * x0

        # Only return the result if it's really the square root (and so
        # self is actually quadratic nonresidue)
        if result.square().eq(self):
            return CtOption(
                result,
                True,
            )

        return CtOption(
            None,
            False,
        )
