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
        return self.infinity

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


class G2Projective:
    def __init__(self, x: Fp2, y: Fp2, z: Fp2):
        self.x = x
        self.y = y
        self.z = z

    # Returns the identity of the group: the point at infinity.
    def identity():
        return G2Projective(Fp2.zero(), Fp2.one(), Fp2.zero())

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
