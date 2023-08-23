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

    def zero():
        return Fp12(Fp6.zero(), Fp6.zero())

    def is_zero(self):
        return self.c0.is_zero() and self.c1.is_zero()

    def one():
        return Fp12(Fp6.one(), Fp6.zero())

    def default():
        return Fp12.zero()

    def eq(self, other):
        return self.c0 == other.c0 and self.c1 == other.c1 and self.c2 == other.c2

    @staticmethod
    def random(rng):
        return Fp12(Fp6.random(rng), Fp6.random(rng))

    def mul_by_014(self, c0: Fp2, c1: Fp2, c4: Fp2):
        aa = self.c0.mul_by_01(c0, c1)
        bb = self.c1.mul_by_1(c4)
        o = c1 + c4
        c1 = self.c1 + self.c0
        c1 = c1.mul_by_01(c0, o)
        c1 = c1 - aa - bb
        c0 = bb
        c0 = c0.mul_by_nonresidue()
        c0 = c0 + aa

        Fp12(c0, c1)

    def conjugate(self):
        return Fp12(self.c0, -self.c1)

    # Raises this element to p.
    def frobenius_map(self):
        c0 = self.c0.frobenius_map()
        c1 = self.c1.frobenius_map()

        # c1 = c1 * (u + 1)^((p - 1) / 6)
        c1 = c1 * Fp6.from_fp2(
            Fp2(
                Fp(
                    [
                        0x0708_9552_B319_D465,
                        0xC669_5F92_B50A_8313,
                        0x97E8_3CCC_D117_228F,
                        0xA35B_AECA_B2DC_29EE,
                        0x1CE3_93EA_5DAA_CE4D,
                        0x08F2_220F_B0FB_66EB,
                    ]
                ),
                Fp(
                    [
                        0xB2F6_6AAD_4CE5_D646,
                        0x5842_A06B_FC49_7CEC,
                        0xCF48_95D4_2599_D394,
                        0xC11B_9CBA_40A8_E8D0,
                        0x2E38_13CB_E5A0_DE89,
                        0x110E_EFDA_8884_7FAF,
                    ]
                ),
            )
        )

        return Fp12(c0, c1)
