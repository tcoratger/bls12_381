from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64, CtOption
from src.fp import Fp
from src.fp2 import Fp2


# This represents an element $c_0 + c_1 v + c_2 v^2$ of $\mathbb{F}_{p^6} = \mathbb{F}_{p^2} / v^3 - u - 1$.
class Fp6:
    def __init__(self, c0: Fp2, c1: Fp2, c2: Fp2):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return self.neg()

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def from_fp(f: Fp):
        return Fp6(Fp2.from_fp(f), Fp2.zero(), Fp2.zero())

    def is_zero(self):
        return self.c0.is_zero() and self.c1.is_zero() and self.c2.is_zero()

    def from_fp2(f: Fp2):
        return Fp6(f, Fp2.zero(), Fp2.zero())

    def eq(self, other):
        return self.c0.eq(other.c0) and self.c1.eq(other.c1) and self.c2.eq(other.c2)

    def zero():
        return Fp6(Fp2.zero(), Fp2.zero(), Fp2.zero())

    def one():
        return Fp6(Fp2.one(), Fp2.zero(), Fp2.zero())

    def default():
        return Fp6.zero()

    @staticmethod
    def random(rng):
        return Fp6(Fp2.random(rng), Fp2.random(rng), Fp2.random(rng))

    def mul_by_1(self, c1: Fp2):
        return Fp6((self.c2 * c1).mul_by_nonresidue(), self.c0 * c1, self.c1 * c1)

    def mul_by_01(self, c0: Fp2, c1: Fp2):
        a_a = self.c0 * c0
        b_b = self.c1 * c1
        t1 = (self.c2 * c1).mul_by_nonresidue() + a_a
        t2 = (c0 + c1) * (self.c0 + self.c1) - a_a - b_b
        t3 = self.c2 * c0 + b_b
        return Fp6(t1, t2, t3)

    # Multiply by quadratic nonresidue v.
    def mul_by_nonresidue(self):
        # Given a + bv + cv^2, this produces
        #     av + bv^2 + cv^3
        # but because v^3 = u + 1, we have
        #     c(u + 1) + av + v^2

        return Fp6(self.c2.mul_by_nonresidue(), self.c0, self.c1)

    # Raises this element to p.
    def frobenius_map(self):
        c0 = self.c0.frobenius_map()
        c1 = self.c1.frobenius_map()
        c2 = self.c2.frobenius_map()

        # c1 = c1 * (u + 1)^((p - 1) / 3)
        c1 = c1 * Fp2(
            Fp.zero(),
            Fp(
                [
                    0xCD03_C9E4_8671_F071,
                    0x5DAB_2246_1FCD_A5D2,
                    0x5870_42AF_D385_1B95,
                    0x8EB6_0EBE_01BA_CB9E,
                    0x03F9_7D6E_83D0_50D2,
                    0x18F0_2065_5463_8741,
                ]
            ),
        )

        # c2 = c2 * (u + 1)^((2p - 2) / 3)
        c2 = c2 * Fp2(
            Fp(
                [
                    0x890D_C9E4_8675_45C3,
                    0x2AF3_2253_3285_A5D5,
                    0x5088_0866_309B_7E2C,
                    0xA20D_1B8C_7E88_1024,
                    0x14E4_F04F_E2DB_9068,
                    0x14E5_6D3F_1564_853A,
                ]
            ),
            Fp.zero(),
        )

        return Fp6(c0, c1, c2)
