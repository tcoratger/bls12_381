from src.fp import Fp
from src.utils import (
    sbb,
    mac,
    adc,
    wrapping_mul_u64,
    wrapping_sub_u64,
    CtOption,
    Choice,
)


# This is an element of $\mathbb{G}_1$ represented in the affine coordinate space.
# It is ideal to keep elements in this representation to reduce memory usage and
# improve performance through the use of mixed curve model arithmetic.
# Values of `G1Affine` are guaranteed to be in the $q$-order subgroup unless an
# "unchecked" API was misused.
class G1Affine:
    def __init__(self, x: Fp, y: Fp, inf: Choice):
        self.x = x
        self.y = y
        self.infinity = inf

    def __neg__(self):
        return self.neg()

    def __add__(self, rhs):
        return add_mixed(rhs, self)

    def identity():
        return G1Affine(Fp.zero(), Fp.one(), Choice(1))

    def is_identity(self):
        return self.infinity

    def default():
        return G1Affine.identity()

    def conditional_select(a, b, choice: Choice):
        return G1Affine(
            Fp.conditional_select(a.x, b.x, choice),
            Fp.conditional_select(a.y, b.y, choice),
            b.infinity if choice.value else a.infinity,
        )

    # The only cases in which two points are equal are
    # 1. infinity is set on both
    # 2. infinity is not set on both, and their coordinates are equal
    def eq(self, other):
        return (self.infinity.value and other.infinity.value) or (
            not self.infinity.value
            and not other.infinity.value
            and self.x.eq(other.x)
            and self.y.eq(other.y)
        )

    def from_g1_projective(p):
        zinv = p.z.invert()
        if zinv.choice:
            zinv = zinv.value
        else:
            zinv = Fp.zero()
        x = p.x * zinv
        y = p.y * zinv

        tmp = G1Affine(x, y, Choice(0))

        return G1Affine.conditional_select(
            tmp, G1Affine.identity(), Choice(1) if zinv.is_zero() else Choice(0)
        )

    def neg(self):
        return G1Affine(
            self.x,
            Fp.conditional_select(-self.y, Fp.one(), self.infinity),
            self.infinity,
        )

    # Returns true if this point is on the curve. This should always return
    # true unless an "unchecked" API was used.
    def is_on_curve(self):
        # y^2 - x^3 ?= 4
        return (self.y.square() - (self.x.square() * self.x)).eq(B) or self.infinity

    # Returns a fixed generator of the group. See [`notes::design`](notes/design/index.html#fixed-generators)
    # for how this generator is chosen.
    def generator():
        return G1Affine(
            Fp(
                [
                    0x5CB3_8790_FD53_0C16,
                    0x7817_FC67_9976_FFF5,
                    0x154F_95C7_143B_A1C1,
                    0xF0AE_6ACD_F3D0_E747,
                    0xEDCE_6ECC_21DB_F440,
                    0x1201_7741_9E0B_FB75,
                ]
            ),
            Fp(
                [
                    0xBAAC_93D5_0CE7_2271,
                    0x8C22_631A_7918_FD8E,
                    0xDD59_5F13_5707_25CE,
                    0x51AC_5829_5040_5194,
                    0x0E1C_8C3F_AD00_59C0,
                    0x0BBC_3EFC_5008_A26A,
                ]
            ),
            Choice(0),
        )


# A nontrivial third root of unity in Fp
BETA = Fp(
    [
        0x30F1_361B_798A_64E8,
        0xF3B8_DDAB_7ECE_5A2A,
        0x16A8_CA3A_C615_77F7,
        0xC26A_2FF8_74FD_029B,
        0x3636_B766_6070_1C6E,
        0x051B_A4AB_241B_6160,
    ]
)


# This is an element of $\mathbb{G}_1$ represented in the projective coordinate space.
class G1Projective:
    def __init__(self, x: Fp, y: Fp, z: Fp):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        if isinstance(rhs, G1Projective):
            return self.add(rhs)
        elif isinstance(rhs, G1Affine):
            return add_mixed(self, rhs)
        elif isinstance(self, G1Affine):
            return add_mixed(rhs, self)
        else:
            raise ValueError("Unsupported type for addition")

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def identity():
        return G1Projective(Fp.zero(), Fp.one(), Fp.zero())

    def is_identity(self):
        return self.z.is_zero()

    def default():
        return G1Projective.identity()

    def from_g1_affine(p):
        return G1Projective(
            p.x, p.y, Fp.conditional_select(Fp.one(), Fp.zero(), p.infinity)
        )

    def conditional_select(a, b, choice: Choice):
        return G1Projective(
            Fp.conditional_select(a.x, b.x, choice),
            Fp.conditional_select(a.y, b.y, choice),
            Fp.conditional_select(a.z, b.z, choice),
        )

    def neg(self):
        return G1Projective(self.x, -self.y, self.z)

    def sub(self, rhs):
        return self + (-rhs)

    # Returns true if this point is on the curve. This should always return
    # true unless an "unchecked" API was used.
    def is_on_curve(self):
        # Y^2 Z = X^3 + b Z^3
        return (self.y.square() * self.z).eq(
            self.x.square() * self.x + self.z.square() * self.z * B
        ) or self.z.is_zero()

    def generator():
        return G1Projective(
            Fp(
                [
                    0x5CB3_8790_FD53_0C16,
                    0x7817_FC67_9976_FFF5,
                    0x154F_95C7_143B_A1C1,
                    0xF0AE_6ACD_F3D0_E747,
                    0xEDCE_6ECC_21DB_F440,
                    0x1201_7741_9E0B_FB75,
                ]
            ),
            Fp(
                [
                    0xBAAC_93D5_0CE7_2271,
                    0x8C22_631A_7918_FD8E,
                    0xDD59_5F13_5707_25CE,
                    0x51AC_5829_5040_5194,
                    0x0E1C_8C3F_AD00_59C0,
                    0x0BBC_3EFC_5008_A26A,
                ]
            ),
            Fp.one(),
        )

    def eq(self, other):
        # Is (xz, yz, z) equal to (x'z', y'z', z') when converted to affine?

        x1 = self.x * other.z
        x2 = other.x * self.z

        y1 = self.y * other.z
        y2 = other.y * self.z

        self_is_zero = self.z.is_zero()
        other_is_zero = other.z.is_zero()

        # Both point at infinity
        return (self_is_zero and other_is_zero) or (
            (not self_is_zero and not other_is_zero) and x1.eq(x2) and y1.eq(y2)
        )
        # Neither point at infinity, coordinates are the same

    # Adds this point to another point.
    def add(self, rhs):
        # Algorithm 7, https://eprint.iacr.org/2015/1060.pdf
        t0 = self.x * rhs.x
        t1 = self.y * rhs.y
        t2 = self.z * rhs.z
        t3 = self.x + self.y
        t4 = rhs.x + rhs.y
        t3 = t3 * t4
        t4 = t0 + t1
        t3 = t3 - t4
        t4 = self.y + self.z
        x3 = rhs.y + rhs.z
        t4 = t4 * x3
        x3 = t1 + t2
        t4 = t4 - x3
        x3 = self.x + self.z
        y3 = rhs.x + rhs.z
        x3 = x3 * y3
        y3 = t0 + t2
        y3 = x3 - y3
        x3 = t0 + t0
        t0 = x3 + t0
        t2 = mul_by_3b(t2)
        z3 = t1 + t2
        t1 = t1 - t2
        y3 = mul_by_3b(y3)
        x3 = t4 * y3
        t2 = t3 * t1
        x3 = t2 - x3
        y3 = y3 * t0
        t1 = t1 * z3
        y3 = t1 + y3
        t0 = t0 * t3
        z3 = z3 * t4
        z3 = z3 + t0

        return G1Projective(x3, y3, z3)

    # Computes the doubling of this point.
    def double(self):
        # Algorithm 9, https://eprint.iacr.org/2015/1060.pdf
        t0 = self.y.square()
        z3 = t0 + t0
        z3 = z3 + z3
        z3 = z3 + z3
        t1 = self.y * self.z
        t2 = self.z.square()
        t2 = mul_by_3b(t2)
        x3 = t2 * z3
        y3 = t0 + t2
        z3 = t1 * z3
        t1 = t2 + t2
        t2 = t1 + t2
        t0 = t0 - t2
        y3 = t0 * y3
        y3 = x3 + y3
        t1 = self.x * self.y
        x3 = t0 * t1
        x3 = x3 + x3

        tmp = G1Projective(x3, y3, z3)

        return G1Projective.conditional_select(
            tmp, G1Projective.identity(), Choice(1) if self.is_identity() else Choice(0)
        )


B = Fp(
    [
        0xAA27_0000_000C_FFF3,
        0x53CC_0032_FC34_000A,
        0x478F_E97A_6B0A_807F,
        0xB1D3_7EBE_E6BA_24D7,
        0x8EC9_733B_BF78_AB2F,
        0x09D6_4551_3D83_DE7E,
    ]
)


# Adds this point to another point in the affine model.
def add_mixed(self: G1Projective, rhs: G1Affine):
    # Algorithm 8, https://eprint.iacr.org/2015/1060.pdf
    t0 = self.x * rhs.x
    t1 = self.y * rhs.y
    t3 = rhs.x + rhs.y
    t4 = self.x + self.y
    t3 = t3 * t4
    t4 = t0 + t1
    t3 = t3 - t4
    t4 = rhs.y * self.z
    t4 = t4 + self.y
    y3 = rhs.x * self.z
    y3 = y3 + self.x
    x3 = t0 + t0
    t0 = x3 + t0
    t2 = mul_by_3b(self.z)
    z3 = t1 + t2
    t1 = t1 - t2
    y3 = mul_by_3b(y3)
    x3 = t4 * y3
    t2 = t3 * t1
    x3 = t2 - x3
    y3 = y3 * t0
    t1 = t1 * z3
    y3 = t1 + y3
    t0 = t0 * t3
    z3 = z3 * t4
    z3 = z3 + t0

    tmp = G1Projective(x3, y3, z3)

    return G1Projective.conditional_select(tmp, self, rhs.is_identity())


def mul_by_3b(a: Fp):
    a = a + a  # 2
    a = a + a  # 4

    return a + a + a  # 12
