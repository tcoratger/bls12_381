from src.fp import Fp
from src.fp2 import Fp2
from src.utils import (
    sbb,
    mac,
    adc,
    wrapping_mul_u64,
    wrapping_sub_u64,
    CtOption,
    Choice,
    BLS_X,
    BLS_X_IS_NEGATIVE,
)
from src.scalar import Scalar


# This is an element of $\mathbb{G}_2$ represented in the affine coordinate space.
# It is ideal to keep elements in this representation to reduce memory usage and
# improve performance through the use of mixed curve model arithmetic.
#
# Values of `G2Affine` are guaranteed to be in the $q$-order subgroup unless an
# "unchecked" API was misused.
class G2Affine:
    def __init__(self, x: Fp2, y: Fp2, inf: Choice):
        self.x = x
        self.y = y
        self.infinity = inf

    def __add__(self, rhs):
        return add_mixed(rhs, self)

    def __neg__(self):
        return self.neg()

    def __mul__(lhs, rhs):
        if isinstance(rhs, Scalar) and isinstance(lhs, G2Affine):
            return G2Projective.from_g2_affine(lhs).multiply(rhs.to_bytes())
        elif isinstance(lhs, G2Affine):
            return G2Projective.from_g2_affine(lhs).multiply(rhs)
        else:
            raise ValueError("Unsupported type for multiplication")

    def identity():
        return G2Affine(Fp2.zero(), Fp2.one(), Choice(1))

    def default():
        return G2Affine.identity()

    def eq(self, other):
        return (self.infinity.value and other.infinity.value) or (
            (not self.infinity.value)
            and (not other.infinity.value)
            and self.x.eq(other.x)
            and self.y.eq(other.y)
        )

    def conditional_select(a, b, choice: Choice):
        return G2Affine(
            Fp2.conditional_select(a.x, b.x, choice),
            Fp2.conditional_select(a.y, b.y, choice),
            Choice.conditional_select(a.infinity, b.infinity, choice),
        )

    # Returns true if this element is the identity (the point at infinity).
    def is_identity(self):
        return self.infinity.value == 1

    # Returns true if this point is on the curve. This should always return
    # true unless an "unchecked" API was used.
    def is_on_curve(self):
        return (self.y.square() - (self.x.square() * self.x)).eq(B) or self.infinity

    # Returns a fixed generator of the group. See [`notes::design`](notes/design/index.html#fixed-generators)
    # for how this generator is chosen.
    def generator():
        return G2Affine(
            Fp2(
                Fp(
                    [
                        0xF5F2_8FA2_0294_0A10,
                        0xB3F5_FB26_87B4_961A,
                        0xA1A8_93B5_3E2A_E580,
                        0x9894_999D_1A3C_AEE9,
                        0x6F67_B763_1863_366B,
                        0x0581_9192_4350_BCD7,
                    ]
                ),
                Fp(
                    [
                        0xA5A9_C075_9E23_F606,
                        0xAAA0_C59D_BCCD_60C3,
                        0x3BB1_7E18_E286_7806,
                        0x1B1A_B6CC_8541_B367,
                        0xC2B6_ED0E_F215_8547,
                        0x1192_2A09_7360_EDF3,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x4C73_0AF8_6049_4C4A,
                        0x597C_FA1F_5E36_9C5A,
                        0xE7E6_856C_AA0A_635A,
                        0xBBEF_B5E9_6E0D_495F,
                        0x07D3_A975_F0EF_25A2,
                        0x0083_FD8E_7E80_DAE5,
                    ]
                ),
                Fp(
                    [
                        0xADC0_FC92_DF64_B05D,
                        0x18AA_270A_2B14_61DC,
                        0x86AD_AC6A_3BE4_EBA0,
                        0x7949_5C4E_C93D_A33A,
                        0xE717_5850_A43C_CAED,
                        0x0B2B_C2A1_63DE_1BF2,
                    ]
                ),
            ),
            Choice(0),
        )

    def from_g2_projective(p):
        zinv = p.z.invert()
        if zinv.choice:
            zinv = zinv.value
        else:
            zinv = Fp2.zero()

        x = p.x * zinv
        y = p.y * zinv

        tmp = G2Affine(x, y, Choice(0))

        return G2Affine.conditional_select(
            tmp, G2Affine.identity(), Choice(1) if zinv.is_zero() else Choice(0)
        )

    def neg(self):
        return G2Affine(
            self.x,
            Fp2.conditional_select(-self.y, Fp2.one(), self.infinity),
            self.infinity,
        )

    # Returns true if this point is free of an $h$-torsion component, and so it
    # exists within the $q$-order subgroup $\mathbb{G}_2$. This should always return true
    # unless an "unchecked" API was used.
    def is_torsion_free(self):
        # Algorithm from Section 4 of https://eprint.iacr.org/2021/1130
        # Updated proof of correctness in https://eprint.iacr.org/2022/352

        # Check that psi(P) == [x] P
        p = G2Projective.from_g2_affine(self)
        return p.psi().eq(p.mul_by_x())


class G2Projective:
    def __init__(self, x: Fp2, y: Fp2, z: Fp2):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        if isinstance(rhs, G2Projective):
            return self.add(rhs)
        elif isinstance(rhs, G2Affine):
            return add_mixed(self, rhs)
        else:
            raise ValueError("Unsupported type for addition")

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(lhs, rhs):
        if isinstance(rhs, Scalar):
            return lhs.multiply(rhs.to_bytes())
        elif isinstance(lhs, Scalar):
            return rhs.multiply(lhs.to_bytes())
        else:
            return lhs.multiply(rhs)

    # Returns the identity of the group: the point at infinity.
    def identity():
        return G2Projective(Fp2.zero(), Fp2.one(), Fp2.zero())

    # Returns true if this element is the identity (the point at infinity).
    def is_identity(self):
        return self.z.is_zero()

    # Returns a fixed generator of the group. See [`notes::design`](notes/design/index.html#fixed-generators)
    # for how this generator is chosen.
    def generator():
        return G2Projective(
            Fp2(
                Fp(
                    [
                        0xF5F2_8FA2_0294_0A10,
                        0xB3F5_FB26_87B4_961A,
                        0xA1A8_93B5_3E2A_E580,
                        0x9894_999D_1A3C_AEE9,
                        0x6F67_B763_1863_366B,
                        0x0581_9192_4350_BCD7,
                    ]
                ),
                Fp(
                    [
                        0xA5A9_C075_9E23_F606,
                        0xAAA0_C59D_BCCD_60C3,
                        0x3BB1_7E18_E286_7806,
                        0x1B1A_B6CC_8541_B367,
                        0xC2B6_ED0E_F215_8547,
                        0x1192_2A09_7360_EDF3,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x4C73_0AF8_6049_4C4A,
                        0x597C_FA1F_5E36_9C5A,
                        0xE7E6_856C_AA0A_635A,
                        0xBBEF_B5E9_6E0D_495F,
                        0x07D3_A975_F0EF_25A2,
                        0x0083_FD8E_7E80_DAE5,
                    ]
                ),
                Fp(
                    [
                        0xADC0_FC92_DF64_B05D,
                        0x18AA_270A_2B14_61DC,
                        0x86AD_AC6A_3BE4_EBA0,
                        0x7949_5C4E_C93D_A33A,
                        0xE717_5850_A43C_CAED,
                        0x0B2B_C2A1_63DE_1BF2,
                    ]
                ),
            ),
            Fp2.one(),
        )

    # Returns true if this point is on the curve. This should always return
    # true unless an "unchecked" API was used.
    def is_on_curve(self):
        # Y^2 Z = X^3 + b Z^3
        return (self.y.square() * self.z).eq(
            (self.x.square() * self.x + self.z.square() * self.z * B)
        ) or self.z.is_zero()

    def eq(self, other):
        # Is (xz, yz, z) equal to (x'z', y'z', z') when converted to affine?
        x1 = self.x * other.z
        x2 = other.x * self.z

        y1 = self.y * other.z
        y2 = other.y * self.z

        self_is_zero = self.z.is_zero()
        other_is_zero = other.z.is_zero()

        return (self_is_zero and other_is_zero) or (
            not self_is_zero and not other_is_zero and x1.eq(x2) and y1.eq(y2)
        )

    def conditional_select(a, b, choice: Choice):
        return G2Projective(
            Fp2.conditional_select(a.x, b.x, choice),
            Fp2.conditional_select(a.y, b.y, choice),
            Fp2.conditional_select(a.z, b.z, choice),
        )

    def from_g2_affine(a):
        return G2Projective(
            a.x, a.y, Fp2.conditional_select(Fp2.one(), Fp2.zero(), a.infinity)
        )

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

        tmp = G2Projective(
            x3,
            y3,
            z3,
        )

        return G2Projective.conditional_select(
            tmp, G2Projective.identity(), Choice(1) if self.is_identity() else Choice(0)
        )

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

        return G2Projective(
            x3,
            y3,
            z3,
        )

    def neg(self):
        return G2Projective(self.x, -self.y, self.z)

    def sub(self, rhs):
        return self + (-rhs)

    def multiply(self, by):
        acc = G2Projective.identity()

        # This is a simple double-and-add implementation of point
        # multiplication, moving from most significant to least
        # significant bit of the scalar.

        # We skip the leading bit because it's always unset for Fq
        # elements.

        first_bit = True

        for byte in reversed(by):
            for i in range(7, -1, -1):
                if first_bit:
                    first_bit = False
                    continue
                bit = (byte >> i) & 1
                acc = acc.double()
                acc = G2Projective.conditional_select(
                    acc, acc + self, Choice(1) if bit else Choice(0)
                )

        return acc

    def psi(self):
        # 1 / ((u+1) ^ ((q-1)/3))
        psi_coeff_x = Fp2(
            Fp.zero(),
            Fp(
                (
                    [
                        0x890DC9E4867545C3,
                        0x2AF322533285A5D5,
                        0x50880866309B7E2C,
                        0xA20D1B8C7E881024,
                        0x14E4F04FE2DB9068,
                        0x14E56D3F1564853A,
                    ]
                )
            ),
        )
        # 1 / ((u+1) ^ (p-1)/2)
        psi_coeff_y = Fp2(
            Fp(
                [
                    0x3E2F585DA55C9AD1,
                    0x4294213D86C18183,
                    0x382844C88B623732,
                    0x92AD2AFD19103E18,
                    0x1D794E4FAC7CF0B9,
                    0x0BD592FC7D825EC8,
                ]
            ),
            Fp(
                [
                    0x7BCFA7A25AA30FDA,
                    0xDC17DEC12A927E7C,
                    0x2F088DD86B4EBEF1,
                    0xD1CA2087DA74D4A7,
                    0x2DA2596696CEBC1D,
                    0x0E2B7EEDBBFD87D2,
                ]
            ),
        )
        return G2Projective(
            # x = frobenius(x)/((u+1)^((p-1)/3))
            self.x.frobenius_map() * psi_coeff_x,
            # y = frobenius(y)/(u+1)^((p-1)/2)
            self.y.frobenius_map() * psi_coeff_y,
            # z = frobenius(z)
            self.z.frobenius_map(),
        )

    def mul_by_x(self):
        xself = G2Projective.identity()

        # # NOTE: in BLS12-381 we can just skip the first bit.
        x = BLS_X >> 1
        tmp = self

        while x != 0:
            tmp = tmp.double()
            if x % 2 == 1:
                xself += tmp
            x >>= 1

        # finally, flip the sign
        if BLS_X_IS_NEGATIVE:
            xself = -xself

        return xself


# Adds this point to another point in the affine model.
def add_mixed(self: G2Projective, rhs: G2Affine):
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

    tmp = G2Projective(
        x3,
        y3,
        z3,
    )

    return G2Projective.conditional_select(
        tmp, self, Choice(1) if rhs.is_identity() else Choice(0)
    )


def mul_by_3b(x: Fp2):
    return x * B3


B = Fp2(
    Fp(
        [
            0xAA27_0000_000C_FFF3,
            0x53CC_0032_FC34_000A,
            0x478F_E97A_6B0A_807F,
            0xB1D3_7EBE_E6BA_24D7,
            0x8EC9_733B_BF78_AB2F,
            0x09D6_4551_3D83_DE7E,
        ]
    ),
    Fp(
        [
            0xAA27_0000_000C_FFF3,
            0x53CC_0032_FC34_000A,
            0x478F_E97A_6B0A_807F,
            0xB1D3_7EBE_E6BA_24D7,
            0x8EC9_733B_BF78_AB2F,
            0x09D6_4551_3D83_DE7E,
        ]
    ),
)

B3 = Fp2.add(Fp2.add(B, B), B)
