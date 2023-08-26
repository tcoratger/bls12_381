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
        return (self.infinity and other.infinity) or (
            not self.infinity
            and not other.infinity
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

        return G1Affine(
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

    def identity():
        return G1Projective(Fp.zero(), Fp.one(), Fp.zero())

    def is_identity(self):
        return self.z.is_zero()

    def default():
        return G1Projective.identity()

    def conditional_select(a, b, choice: Choice):
        return G1Projective(
            Fp.conditional_select(a.x, b.x, choice),
            Fp.conditional_select(a.y, b.y, choice),
            Fp.conditional_select(a.z, b.z, choice),
        )

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
