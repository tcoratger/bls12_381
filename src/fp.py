from typing import List
from src.utils import sbb, mac, adc, wrapping_mul_u64, wrapping_sub_u64


class CtOption:
    def __init__(self, value=None, choice=False):
        self.value = value
        self.choice = choice


class Fp:
    def __init__(self, array):
        self.array = array

    def __mul__(self, other):
        return self.mul(other)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __neg__(self):
        return self.neg()

    @staticmethod
    def zero():
        return Fp([0] * 6)

    @staticmethod
    def default():
        return Fp.zero()

    def one():
        return R

    def is_zero(self):
        return Fp.eq(self, Fp.zero())

    def eq(self, other):
        return (
            self.array[0] == other.array[0]
            and self.array[1] == other.array[1]
            and self.array[2] == other.array[2]
            and self.array[3] == other.array[3]
            and self.array[4] == other.array[4]
            and self.array[5] == other.array[5]
        )

    def neq(self, other):
        return not Fp.eq(self, other)

    @staticmethod
    def montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11):
        # The Montgomery reduction here is based on Algorithm 14.32 in
        # Handbook of Applied Cryptography
        # <http://cacr.uwaterloo.ca/hac/about/chap14.pdf>.

        k = wrapping_mul_u64(t0, INV)
        _, carry = mac(t0, k, MODULUS[0], 0)
        r1, carry = mac(t1, k, MODULUS[1], carry)
        r2, carry = mac(t2, k, MODULUS[2], carry)
        r3, carry = mac(t3, k, MODULUS[3], carry)
        r4, carry = mac(t4, k, MODULUS[4], carry)
        r5, carry = mac(t5, k, MODULUS[5], carry)
        r6, r7 = adc(t6, 0, carry)

        k = wrapping_mul_u64(r1, INV)
        _, carry = mac(r1, k, MODULUS[0], 0)
        r2, carry = mac(r2, k, MODULUS[1], carry)
        r3, carry = mac(r3, k, MODULUS[2], carry)
        r4, carry = mac(r4, k, MODULUS[3], carry)
        r5, carry = mac(r5, k, MODULUS[4], carry)
        r6, carry = mac(r6, k, MODULUS[5], carry)
        r7, r8 = adc(t7, r7, carry)

        k = wrapping_mul_u64(r2, INV)
        _, carry = mac(r2, k, MODULUS[0], 0)
        r3, carry = mac(r3, k, MODULUS[1], carry)
        r4, carry = mac(r4, k, MODULUS[2], carry)
        r5, carry = mac(r5, k, MODULUS[3], carry)
        r6, carry = mac(r6, k, MODULUS[4], carry)
        r7, carry = mac(r7, k, MODULUS[5], carry)
        r8, r9 = adc(t8, r8, carry)

        k = wrapping_mul_u64(r3, INV)
        _, carry = mac(r3, k, MODULUS[0], 0)
        r4, carry = mac(r4, k, MODULUS[1], carry)
        r5, carry = mac(r5, k, MODULUS[2], carry)
        r6, carry = mac(r6, k, MODULUS[3], carry)
        r7, carry = mac(r7, k, MODULUS[4], carry)
        r8, carry = mac(r8, k, MODULUS[5], carry)
        r9, r10 = adc(t9, r9, carry)

        k = wrapping_mul_u64(r4, INV)
        _, carry = mac(r4, k, MODULUS[0], 0)
        r5, carry = mac(r5, k, MODULUS[1], carry)
        r6, carry = mac(r6, k, MODULUS[2], carry)
        r7, carry = mac(r7, k, MODULUS[3], carry)
        r8, carry = mac(r8, k, MODULUS[4], carry)
        r9, carry = mac(r9, k, MODULUS[5], carry)
        r10, r11 = adc(t10, r10, carry)

        k = wrapping_mul_u64(r5, INV)
        _, carry = mac(r5, k, MODULUS[0], 0)
        r6, carry = mac(r6, k, MODULUS[1], carry)
        r7, carry = mac(r7, k, MODULUS[2], carry)
        r8, carry = mac(r8, k, MODULUS[3], carry)
        r9, carry = mac(r9, k, MODULUS[4], carry)
        r10, carry = mac(r10, k, MODULUS[5], carry)
        r11, _ = adc(t11, r11, carry)

        return Fp([r6, r7, r8, r9, r10, r11]).subtract_p()

    def mul(self, rhs):
        t0, carry = mac(0, self.array[0], rhs.array[0], 0)
        t1, carry = mac(0, self.array[0], rhs.array[1], carry)
        t2, carry = mac(0, self.array[0], rhs.array[2], carry)
        t3, carry = mac(0, self.array[0], rhs.array[3], carry)
        t4, carry = mac(0, self.array[0], rhs.array[4], carry)
        t5, t6 = mac(0, self.array[0], rhs.array[5], carry)

        t1, carry = mac(t1, self.array[1], rhs.array[0], 0)
        t2, carry = mac(t2, self.array[1], rhs.array[1], carry)
        t3, carry = mac(t3, self.array[1], rhs.array[2], carry)
        t4, carry = mac(t4, self.array[1], rhs.array[3], carry)
        t5, carry = mac(t5, self.array[1], rhs.array[4], carry)
        t6, t7 = mac(t6, self.array[1], rhs.array[5], carry)

        t2, carry = mac(t2, self.array[2], rhs.array[0], 0)
        t3, carry = mac(t3, self.array[2], rhs.array[1], carry)
        t4, carry = mac(t4, self.array[2], rhs.array[2], carry)
        t5, carry = mac(t5, self.array[2], rhs.array[3], carry)
        t6, carry = mac(t6, self.array[2], rhs.array[4], carry)
        t7, t8 = mac(t7, self.array[2], rhs.array[5], carry)

        t3, carry = mac(t3, self.array[3], rhs.array[0], 0)
        t4, carry = mac(t4, self.array[3], rhs.array[1], carry)
        t5, carry = mac(t5, self.array[3], rhs.array[2], carry)
        t6, carry = mac(t6, self.array[3], rhs.array[3], carry)
        t7, carry = mac(t7, self.array[3], rhs.array[4], carry)
        t8, t9 = mac(t8, self.array[3], rhs.array[5], carry)

        t4, carry = mac(t4, self.array[4], rhs.array[0], 0)
        t5, carry = mac(t5, self.array[4], rhs.array[1], carry)
        t6, carry = mac(t6, self.array[4], rhs.array[2], carry)
        t7, carry = mac(t7, self.array[4], rhs.array[3], carry)
        t8, carry = mac(t8, self.array[4], rhs.array[4], carry)
        t9, t10 = mac(t9, self.array[4], rhs.array[5], carry)

        t5, carry = mac(t5, self.array[5], rhs.array[0], 0)
        t6, carry = mac(t6, self.array[5], rhs.array[1], carry)
        t7, carry = mac(t7, self.array[5], rhs.array[2], carry)
        t8, carry = mac(t8, self.array[5], rhs.array[3], carry)
        t9, carry = mac(t9, self.array[5], rhs.array[4], carry)
        t10, t11 = mac(t10, self.array[5], rhs.array[5], carry)

        return Fp.montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11)

    def subtract_p(self):
        r0, borrow = sbb(self.array[0], MODULUS[0], 0)
        r1, borrow = sbb(self.array[1], MODULUS[1], borrow)
        r2, borrow = sbb(self.array[2], MODULUS[2], borrow)
        r3, borrow = sbb(self.array[3], MODULUS[3], borrow)
        r4, borrow = sbb(self.array[4], MODULUS[4], borrow)
        r5, borrow = sbb(self.array[5], MODULUS[5], borrow)

        # If underflow occurred on the final limb, borrow = 0xfff...fff, otherwise
        # borrow = 0x000...000. Thus, we use it as a mask!
        r0 = (self.array[0] & borrow) | (r0 & ~borrow)
        r1 = (self.array[1] & borrow) | (r1 & ~borrow)
        r2 = (self.array[2] & borrow) | (r2 & ~borrow)
        r3 = (self.array[3] & borrow) | (r3 & ~borrow)
        r4 = (self.array[4] & borrow) | (r4 & ~borrow)
        r5 = (self.array[5] & borrow) | (r5 & ~borrow)

        return Fp([r0, r1, r2, r3, r4, r5])

    def from_bytes(bytes):
        tmp = Fp([0, 0, 0, 0, 0, 0])

        tmp.array[5] = int.from_bytes(bytes[0:8], byteorder="big")
        tmp.array[4] = int.from_bytes(bytes[8:16], byteorder="big")
        tmp.array[3] = int.from_bytes(bytes[16:24], byteorder="big")
        tmp.array[2] = int.from_bytes(bytes[24:32], byteorder="big")
        tmp.array[1] = int.from_bytes(bytes[32:40], byteorder="big")
        tmp.array[0] = int.from_bytes(bytes[40:48], byteorder="big")

        # Try to subtract the modulus
        _, borrow = sbb(tmp.array[0], MODULUS[0], 0)
        _, borrow = sbb(tmp.array[1], MODULUS[1], borrow)
        _, borrow = sbb(tmp.array[2], MODULUS[2], borrow)
        _, borrow = sbb(tmp.array[3], MODULUS[3], borrow)
        _, borrow = sbb(tmp.array[4], MODULUS[4], borrow)
        _, borrow = sbb(tmp.array[5], MODULUS[5], borrow)

        # If the element is smaller than MODULUS then the
        # subtraction will underflow, producing a borrow value
        # of 0xffff...ffff. Otherwise, it'll be zero.
        is_some = borrow & 1

        # Convert to Montgomery form by computing
        # (a.R^0 * R^2) / R = a.R
        tmp *= R2

        return CtOption(tmp, is_some)

    def neg(self):
        d0, borrow = sbb(MODULUS[0], self.array[0], 0)
        d1, borrow = sbb(MODULUS[1], self.array[1], borrow)
        d2, borrow = sbb(MODULUS[2], self.array[2], borrow)
        d3, borrow = sbb(MODULUS[3], self.array[3], borrow)
        d4, borrow = sbb(MODULUS[4], self.array[4], borrow)
        d5, _ = sbb(MODULUS[5], self.array[5], borrow)

        # Let's use a mask if `self` was zero, which would mean
        # the result of the subtraction is p.
        mask = wrapping_sub_u64(
            int(
                (
                    (
                        self.array[0]
                        | self.array[1]
                        | self.array[2]
                        | self.array[3]
                        | self.array[4]
                        | self.array[5]
                    )
                    == 0
                )
            )
            & ((1 << 64) - 1),
            1,
        )

        return Fp(
            [
                d0 & mask,
                d1 & mask,
                d2 & mask,
                d3 & mask,
                d4 & mask,
                d5 & mask,
            ]
        )

    def add(self, rhs):
        d0, carry = adc(self.array[0], rhs.array[0], 0)
        d1, carry = adc(self.array[1], rhs.array[1], carry)
        d2, carry = adc(self.array[2], rhs.array[2], carry)
        d3, carry = adc(self.array[3], rhs.array[3], carry)
        d4, carry = adc(self.array[4], rhs.array[4], carry)
        d5, _ = adc(self.array[5], rhs.array[5], carry)

        return Fp([d0, d1, d2, d3, d4, d5]).subtract_p()

    def sub(self, rhs):
        return rhs.neg().add(self)

    @staticmethod
    def random(rng):
        bytes = bytearray(rng.randint(0, 255) for _ in range(96))

        # Parse the random bytes as a big-endian number, to match Fp encoding order.
        limbs = [
            int.from_bytes(bytes[0:8], byteorder="big"),
            int.from_bytes(bytes[8:16], byteorder="big"),
            int.from_bytes(bytes[16:24], byteorder="big"),
            int.from_bytes(bytes[24:32], byteorder="big"),
            int.from_bytes(bytes[32:40], byteorder="big"),
            int.from_bytes(bytes[40:48], byteorder="big"),
            int.from_bytes(bytes[48:56], byteorder="big"),
            int.from_bytes(bytes[56:64], byteorder="big"),
            int.from_bytes(bytes[64:72], byteorder="big"),
            int.from_bytes(bytes[72:80], byteorder="big"),
            int.from_bytes(bytes[80:88], byteorder="big"),
            int.from_bytes(bytes[88:96], byteorder="big"),
        ]

        return Fp.from_u768(limbs)

    @staticmethod
    def from_u768(limbs: List[int]) -> "Fp":
        # We reduce an arbitrary 768-bit number by decomposing it into two 384-bit digits
        # with the higher bits multiplied by 2^384. Thus, we perform two reductions:
        #
        # 1. the lower bits are multiplied by R^2, as normal
        # 2. the upper bits are multiplied by R^2 * 2^384 = R^3
        #
        # and computing their sum in the field. It remains to see that arbitrary 384-bit
        # numbers can be placed into Montgomery form safely using the reduction. The
        # reduction works as long as the product is less than R=2^384 multiplied by
        # the modulus. This holds because for any `c` smaller than the modulus, we have
        # that (2^384 - 1)*c is an acceptable product for the reduction. Therefore, the
        # reduction always works as long as `c` is in the field; in this case, it is either the
        # constant `R2` or `R3`.

        d1 = Fp([limbs[11], limbs[10], limbs[9], limbs[8], limbs[7], limbs[6]])
        d0 = Fp([limbs[5], limbs[4], limbs[3], limbs[2], limbs[1], limbs[0]])

        # Convert to Montgomery form
        return d0 * R2 + d1 * R3

    def square(self):
        # Perform the square operation
        t1, carry = mac(0, self.array[0], self.array[1], 0)
        t2, carry = mac(0, self.array[0], self.array[2], carry)
        t3, carry = mac(0, self.array[0], self.array[3], carry)
        t4, carry = mac(0, self.array[0], self.array[4], carry)
        t5, t6 = mac(0, self.array[0], self.array[5], carry)

        t3, carry = mac(t3, self.array[1], self.array[2], 0)
        t4, carry = mac(t4, self.array[1], self.array[3], carry)
        t5, carry = mac(t5, self.array[1], self.array[4], carry)
        t6, t7 = mac(t6, self.array[1], self.array[5], carry)

        t5, carry = mac(t5, self.array[2], self.array[3], 0)
        t6, carry = mac(t6, self.array[2], self.array[4], carry)
        t7, t8 = mac(t7, self.array[2], self.array[5], carry)

        t7, carry = mac(t7, self.array[3], self.array[4], 0)
        t8, t9 = mac(t8, self.array[3], self.array[5], carry)

        t9, t10 = mac(t9, self.array[4], self.array[5], 0)

        t11 = t10 >> 63 & ((1 << 64) - 1)
        t10 = (t10 << 1) & ((1 << 64) - 1) | (t9 >> 63) & ((1 << 64) - 1)
        t9 = (t9 << 1) & ((1 << 64) - 1) | (t8 >> 63) & ((1 << 64) - 1)
        t8 = (t8 << 1) & ((1 << 64) - 1) | (t7 >> 63) & ((1 << 64) - 1)
        t7 = (t7 << 1) & ((1 << 64) - 1) | (t6 >> 63) & ((1 << 64) - 1)
        t6 = (t6 << 1) & ((1 << 64) - 1) | (t5 >> 63) & ((1 << 64) - 1)
        t5 = (t5 << 1) & ((1 << 64) - 1) | (t4 >> 63) & ((1 << 64) - 1)
        t4 = (t4 << 1) & ((1 << 64) - 1) | (t3 >> 63) & ((1 << 64) - 1)
        t3 = (t3 << 1) & ((1 << 64) - 1) | (t2 >> 63) & ((1 << 64) - 1)
        t2 = (t2 << 1) & ((1 << 64) - 1) | (t1 >> 63) & ((1 << 64) - 1)
        t1 = t1 << 1 & ((1 << 64) - 1)

        t0, carry = mac(0, self.array[0], self.array[0], 0)
        t1, carry = adc(t1, 0, carry)
        t2, carry = mac(t2, self.array[1], self.array[1], carry)
        t3, carry = adc(t3, 0, carry)
        t4, carry = mac(t4, self.array[2], self.array[2], carry)
        t5, carry = adc(t5, 0, carry)
        t6, carry = mac(t6, self.array[3], self.array[3], carry)
        t7, carry = adc(t7, 0, carry)
        t8, carry = mac(t8, self.array[4], self.array[4], carry)
        t9, carry = adc(t9, 0, carry)
        t10, carry = mac(t10, self.array[5], self.array[5], carry)
        t11, _ = adc(t11, 0, carry)

        # Perform Montgomery reduction
        return Fp.montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11)


# p = 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787
MODULUS = [
    0xB9FE_FFFF_FFFF_AAAB,
    0x1EAB_FFFE_B153_FFFF,
    0x6730_D2A0_F6B0_F624,
    0x6477_4B84_F385_12BF,
    0x4B1B_A7B6_434B_ACD7,
    0x1A01_11EA_397F_E69A,
]

# INV = -(p^{-1} mod 2^64) mod 2^64
INV = 0x89F3_FFFC_FFFC_FFFD

# R = 2^384 mod p
R = Fp(
    [
        0x7609_0000_0002_FFFD,
        0xEBF4_000B_C40C_0002,
        0x5F48_9857_53C7_58BA,
        0x77CE_5853_7052_5745,
        0x5C07_1A97_A256_EC6D,
        0x15F6_5EC3_FA80_E493,
    ]
)

# R2 = 2^(384*2) mod p
R2 = Fp(
    [
        0xF4DF_1F34_1C34_1746,
        0x0A76_E6A6_09D1_04F1,
        0x8DE5_476C_4C95_B6D5,
        0x67EB_88A9_939D_83C0,
        0x9A79_3E85_B519_952D,
        0x1198_8FE5_92CA_E3AA,
    ]
)

# R3 = 2^(384*3) mod p
R3 = Fp(
    [
        0xED48_AC6B_D94C_A1E0,
        0x315F_831E_03A7_ADF8,
        0x9A53_352A_615E_29DD,
        0x34C0_4E5E_921E_1761,
        0x2512_D435_6572_4728,
        0x0AA6_3460_9175_5D4D,
    ]
)
