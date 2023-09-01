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


# Represents an element of the scalar field $\mathbb{F}_q$ of the BLS12-381 elliptic
# curve construction.
# The internal representation of this type is four 64-bit unsigned
# integers in little-endian order. `Scalar` values are always in
# Montgomery form; i.e., Scalar(a) = aR mod q, with R = 2^256.
class Scalar:
    def __init__(self, array):
        if len(array) != 4:
            raise ValueError("Scalar array must have exactly 4 elements")
        self.array = array

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def __neg__(self):
        return self.neg()

    def from_u64(val):
        return Scalar([val, 0, 0, 0]) * R2

    def eq(self, other):
        return (
            self.array[0] == other.array[0]
            and self.array[1] == other.array[1]
            and self.array[2] == other.array[2]
            and self.array[3] == other.array[3]
        )

    def conditional_select(a, b, choice: Choice):
        return Scalar(
            [
                choice.value * b.array[i] + (1 - choice.value) * a.array[i]
                for i in range(len(a.array))
            ]
        )

    def zero():
        return Scalar([0, 0, 0, 0])

    def one():
        return R

    # Adds `rhs` to `self`, returning the result.
    def add(self, rhs):
        d0, carry = adc(self.array[0], rhs.array[0], 0)
        d1, carry = adc(self.array[1], rhs.array[1], carry)
        d2, carry = adc(self.array[2], rhs.array[2], carry)
        d3, _ = adc(self.array[3], rhs.array[3], carry)

        # Attempt to subtract the modulus, to ensure the value
        # is smaller than the modulus.
        return Scalar([d0, d1, d2, d3]).sub(MODULUS)

    def sub(self, rhs):
        d0, borrow = sbb(self.array[0], rhs.array[0], 0)
        d1, borrow = sbb(self.array[1], rhs.array[1], borrow)
        d2, borrow = sbb(self.array[2], rhs.array[2], borrow)
        d3, borrow = sbb(self.array[3], rhs.array[3], borrow)

        # If underflow occurred on the final limb, borrow = 0xfff...fff, otherwise
        # borrow = 0x000...000. Thus, we use it as a mask to conditionally add the modulus.
        d0, carry = adc(d0, MODULUS.array[0] & borrow, 0)
        d1, carry = adc(d1, MODULUS.array[1] & borrow, carry)
        d2, carry = adc(d2, MODULUS.array[2] & borrow, carry)
        d3, _ = adc(d3, MODULUS.array[3] & borrow, carry)

        return Scalar([d0, d1, d2, d3])

    @staticmethod
    def montgomery_reduce(r0, r1, r2, r3, r4, r5, r6, r7):
        # The Montgomery reduction here is based on Algorithm 14.32 in
        # Handbook of Applied Cryptography
        # <http://cacr.uwaterloo.ca/hac/about/chap14.pdf>.

        k = wrapping_mul_u64(r0, INV)
        _, carry = mac(r0, k, MODULUS.array[0], 0)
        r1, carry = mac(r1, k, MODULUS.array[1], carry)
        r2, carry = mac(r2, k, MODULUS.array[2], carry)
        r3, carry = mac(r3, k, MODULUS.array[3], carry)
        r4, carry2 = adc(r4, 0, carry)

        k = wrapping_mul_u64(r1, INV)
        _, carry = mac(r1, k, MODULUS.array[0], 0)
        r2, carry = mac(r2, k, MODULUS.array[1], carry)
        r3, carry = mac(r3, k, MODULUS.array[2], carry)
        r4, carry = mac(r4, k, MODULUS.array[3], carry)
        r5, carry2 = adc(r5, carry2, carry)

        k = wrapping_mul_u64(r2, INV)
        _, carry = mac(r2, k, MODULUS.array[0], 0)
        r3, carry = mac(r3, k, MODULUS.array[1], carry)
        r4, carry = mac(r4, k, MODULUS.array[2], carry)
        r5, carry = mac(r5, k, MODULUS.array[3], carry)
        r6, carry2 = adc(r6, carry2, carry)

        k = wrapping_mul_u64(r3, INV)
        _, carry = mac(r3, k, MODULUS.array[0], 0)
        r4, carry = mac(r4, k, MODULUS.array[1], carry)
        r5, carry = mac(r5, k, MODULUS.array[2], carry)
        r6, carry = mac(r6, k, MODULUS.array[3], carry)
        r7, _ = adc(r7, carry2, carry)

        return Scalar([r4, r5, r6, r7]).sub(MODULUS)

    def mul(self, rhs):
        t0, carry = mac(0, self.array[0], rhs.array[0], 0)
        t1, carry = mac(0, self.array[0], rhs.array[1], carry)
        t2, carry = mac(0, self.array[0], rhs.array[2], carry)
        t3, t4 = mac(0, self.array[0], rhs.array[3], carry)

        t1, carry = mac(t1, self.array[1], rhs.array[0], 0)
        t2, carry = mac(t2, self.array[1], rhs.array[1], carry)
        t3, carry = mac(t3, self.array[1], rhs.array[2], carry)
        t4, t5 = mac(t4, self.array[1], rhs.array[3], carry)

        t2, carry = mac(t2, self.array[2], rhs.array[0], 0)
        t3, carry = mac(t3, self.array[2], rhs.array[1], carry)
        t4, carry = mac(t4, self.array[2], rhs.array[2], carry)
        t5, t6 = mac(t5, self.array[2], rhs.array[3], carry)

        t3, carry = mac(t3, self.array[3], rhs.array[0], 0)
        t4, carry = mac(t4, self.array[3], rhs.array[1], carry)
        t5, carry = mac(t5, self.array[3], rhs.array[2], carry)
        t6, t7 = mac(t6, self.array[3], rhs.array[3], carry)

        return Scalar.montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7)

    def neg(self):
        d0, borrow = sbb(MODULUS.array[0], self.array[0], 0)
        d1, borrow = sbb(MODULUS.array[1], self.array[1], borrow)
        d2, borrow = sbb(MODULUS.array[2], self.array[2], borrow)
        d3, _ = sbb(MODULUS.array[3], self.array[3], borrow)

        # Let's use a mask if `self` was zero, which would mean
        # the result of the subtraction is p.
        mask = wrapping_sub_u64(
            int(((self.array[0] | self.array[1] | self.array[2] | self.array[3]) == 0))
            & ((1 << 64) - 1),
            1,
        )

        return Scalar(
            [
                d0 & mask,
                d1 & mask,
                d2 & mask,
                d3 & mask,
            ]
        )

    def to_bytes(self):
        # Turn into canonical form by computing
        # (a.R) / R = a
        tmp = Scalar.montgomery_reduce(
            self.array[0],
            self.array[1],
            self.array[2],
            self.array[3],
            0,
            0,
            0,
            0,
        )

        res = []
        res[0:8] = tmp.array[0].to_bytes(8, "little")
        res[8:16] = tmp.array[1].to_bytes(8, "little")
        res[16:24] = tmp.array[2].to_bytes(8, "little")
        res[24:32] = tmp.array[3].to_bytes(8, "little")

        return res

    def from_bytes(bytes):
        tmp = Scalar([0, 0, 0, 0])

        tmp.array[0] = int.from_bytes(bytes[0:8], byteorder="little")
        tmp.array[1] = int.from_bytes(bytes[8:16], byteorder="little")
        tmp.array[2] = int.from_bytes(bytes[16:24], byteorder="little")
        tmp.array[3] = int.from_bytes(bytes[24:32], byteorder="little")

        # Try to subtract the modulus
        _, borrow = sbb(tmp.array[0], MODULUS.array[0], 0)
        _, borrow = sbb(tmp.array[1], MODULUS.array[1], borrow)
        _, borrow = sbb(tmp.array[2], MODULUS.array[2], borrow)
        _, borrow = sbb(tmp.array[3], MODULUS.array[3], borrow)

        # If the element is smaller than MODULUS then the
        # subtraction will underflow, producing a borrow value
        # of 0xffff...ffff. Otherwise, it'll be zero.
        is_some = (int(borrow) & 0xFF) & 1

        # Convert to Montgomery form by computing
        # (a.R^0 * R^2) / R = a.R
        tmp *= R2

        return CtOption(tmp, Choice(1) if is_some else Choice(0))

    def from_u512(limbs):
        # We reduce an arbitrary 512-bit number by decomposing it into two 256-bit digits
        # with the higher bits multiplied by 2^256. Thus, we perform two reductions

        # 1. the lower bits are multiplied by R^2, as normal
        # 2. the upper bits are multiplied by R^2 * 2^256 = R^3

        # and computing their sum in the field. It remains to see that arbitrary 256-bit
        # numbers can be placed into Montgomery form safely using the reduction. The
        # reduction works so long as the product is less than R=2^256 multiplied by
        # the modulus. This holds because for any `c` smaller than the modulus, we have
        # that (2^256 - 1)*c is an acceptable product for the reduction. Therefore, the
        # reduction always works so long as `c` is in the field; in this case it is either the
        # constant `R2` or `R3`.

        d0 = Scalar([limbs[0], limbs[1], limbs[2], limbs[3]])
        d1 = Scalar([limbs[4], limbs[5], limbs[6], limbs[7]])

        # Convert to Montgomery form
        return d0 * R2 + d1 * R3

    # Converts a 512-bit little endian integer into
    # a `Scalar` by reducing by the modulus.
    def from_bytes_wide(bytes):
        return Scalar.from_u512(
            [
                int.from_bytes(bytes[0:8], byteorder="little"),
                int.from_bytes(bytes[8:16], byteorder="little"),
                int.from_bytes(bytes[16:24], byteorder="little"),
                int.from_bytes(bytes[24:32], byteorder="little"),
                int.from_bytes(bytes[32:40], byteorder="little"),
                int.from_bytes(bytes[40:48], byteorder="little"),
                int.from_bytes(bytes[48:56], byteorder="little"),
                int.from_bytes(bytes[56:64], byteorder="little"),
            ]
        )

    def square(self):
        # Perform the square operation
        t1, carry = mac(0, self.array[0], self.array[1], 0)
        t2, carry = mac(0, self.array[0], self.array[2], carry)
        t3, t4 = mac(0, self.array[0], self.array[3], carry)

        t3, carry = mac(t3, self.array[1], self.array[2], 0)
        t4, t5 = mac(t4, self.array[1], self.array[3], carry)

        t5, t6 = mac(t5, self.array[2], self.array[3], 0)

        t7 = t6 >> 63 & ((1 << 64) - 1)
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
        t7, _ = adc(t7, 0, carry)

        # Perform Montgomery reduction
        return Scalar.montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7)

    def invert(self):
        def square_assign_multi(n, num_times):
            for _ in range(num_times):
                n = n.square()

            return n

        # found using https://github.com/kwantam/addchain
        t0 = self.square()
        t1 = t0 * self
        t16 = t0.square()
        t6 = t16.square()
        t5 = t6 * t0
        t0 = t6 * t16
        t12 = t5 * t16
        t2 = t6.square()
        t7 = t5 * t6
        t15 = t0 * t5
        t17 = t12.square()
        t1 *= t17
        t3 = t7 * t2
        t8 = t1 * t17
        t4 = t8 * t2
        t9 = t8 * t7
        t7 = t4 * t5
        t11 = t4 * t17
        t5 = t9 * t17
        t14 = t7 * t15
        t13 = t11 * t12
        t12 = t11 * t17
        t15 *= t12
        t16 *= t15
        t3 *= t16
        t17 *= t3
        t0 *= t17
        t6 *= t0
        t2 *= t6
        t0 = square_assign_multi(t0, 8)
        t0 *= t17
        t0 = square_assign_multi(t0, 9)
        t0 *= t16
        t0 = square_assign_multi(t0, 9)
        t0 *= t15
        t0 = square_assign_multi(t0, 9)
        t0 *= t15
        t0 = square_assign_multi(t0, 7)
        t0 *= t14
        t0 = square_assign_multi(t0, 7)
        t0 *= t13
        t0 = square_assign_multi(t0, 10)
        t0 *= t12
        t0 = square_assign_multi(t0, 9)
        t0 *= t11
        t0 = square_assign_multi(t0, 8)
        t0 *= t8
        t0 = square_assign_multi(t0, 8)
        t0 *= self
        t0 = square_assign_multi(t0, 14)
        t0 *= t9
        t0 = square_assign_multi(t0, 10)
        t0 *= t8
        t0 = square_assign_multi(t0, 15)
        t0 *= t7
        t0 = square_assign_multi(t0, 10)
        t0 *= t6
        t0 = square_assign_multi(t0, 8)
        t0 *= t5
        t0 = square_assign_multi(t0, 16)
        t0 *= t3
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 7)
        t0 *= t4
        t0 = square_assign_multi(t0, 9)
        t0 *= t2
        t0 = square_assign_multi(t0, 8)
        t0 *= t3
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 8)
        t0 *= t3
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 8)
        t0 *= t2
        t0 = square_assign_multi(t0, 5)
        t0 *= t1
        t0 = square_assign_multi(t0, 5)
        t0 *= t1

        return CtOption(t0, Choice(1) if not self.eq(Scalar.zero()) else Choice(0))

    def pow(self, by):
        res = Scalar.one()
        for e in reversed(by):
            for i in range(63, -1, -1):
                res = res.square()
                tmp = res * self
                res = Scalar.conditional_select(
                    tmp, res, Choice(0) if (((e >> i) & 0x1) & 0xFF) else Choice(1)
                )
        return res

    # Exponentiates `self` by `by`, where `by` is a
    # little-endian order integer exponent.

    # **This operation is variable time with respect
    # to the exponent.** If the exponent is fixed,
    # this operation is effectively constant time.
    def pow_vartime(self, by):
        res = Scalar.one()
        for e in reversed(by):
            for i in range(63, -1, -1):
                res = res.square()

                if ((e >> i) & 1) == 1:
                    res *= self
        return res

    def from_raw(val):
        return Scalar(val) * R2

    def double(self):
        return self + self


# Constant representing the modulus
# q = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
MODULUS = Scalar(
    [
        0xFFFF_FFFF_0000_0001,
        0x53BD_A402_FFFE_5BFE,
        0x3339_D808_09A1_D805,
        0x73ED_A753_299D_7D48,
    ]
)

# The number of bits needed to represent the modulus.
MODULUS_BITS = 255

# GENERATOR = 7 (multiplicative generator of r-1 order, that is also quadratic nonresidue)
GENERATOR = Scalar(
    [
        0x0000_000E_FFFF_FFF1,
        0x17E3_63D3_0018_9C0F,
        0xFF9C_5787_6F84_57B0,
        0x3513_3220_8FC5_A8C4,
    ]
)

# INV = -(q^{-1} mod 2^64) mod 2^64
INV = 0xFFFF_FFFE_FFFF_FFFF

# R = 2^256 mod q
R = Scalar(
    [
        0x0000_0001_FFFF_FFFE,
        0x5884_B7FA_0003_4802,
        0x998C_4FEF_ECBC_4FF5,
        0x1824_B159_ACC5_056F,
    ]
)

# R^2 = 2^512 mod q
R2 = Scalar(
    [
        0xC999_E990_F3F2_9C6D,
        0x2B6C_EDCB_8792_5C23,
        0x05D3_1496_7254_398F,
        0x0748_D9D9_9F59_FF11,
    ]
)

# R^3 = 2^768 mod q
R3 = Scalar(
    [
        0xC62C_1807_439B_73AF,
        0x1B3E_0D18_8CF0_6990,
        0x73D1_3C71_C7B5_F418,
        0x6E2A_5BB9_C8DB_33E9,
    ]
)

# 2^-1
TWO_INV = Scalar(
    [
        0x0000_0000_FFFF_FFFF,
        0xAC42_5BFD_0001_A401,
        0xCCC6_27F7_F65E_27FA,
        0x0C12_58AC_D662_82B7,
    ]
)

# 2^S * t = MODULUS - 1 with t odd
S = 32

# GENERATOR^t where t * 2^s + 1 = q
# with t odd. In other words, this
# is a 2^s root of unity.

# `GENERATOR = 7 mod q` is a generator
# of the q - 1 order multiplicative
# subgroup.
ROOT_OF_UNITY = Scalar(
    [
        0xB9B5_8D8C_5F0E_466A,
        0x5B1B_4C80_1819_D7EC,
        0x0AF5_3AE3_52A3_1E64,
        0x5BF3_ADDA_19E9_B27B,
    ]
)

# ROOT_OF_UNITY^-1
ROOT_OF_UNITY_INV = Scalar(
    [
        0x4256_481A_DCF3_219A,
        0x45F3_7B7F_96B6_CAD3,
        0xF9C3_F1D7_5F7A_3B27,
        0x2D2F_C049_658A_FD43,
    ]
)

# GENERATOR^{2^s} where t * 2^s + 1 = q with t odd.
# In other words, this is a t root of unity.
DELTA = Scalar(
    [
        0x70E3_10D3_D146_F96A,
        0x4B64_C089_19E2_99E6,
        0x51E1_1418_6A8B_970D,
        0x6185_D066_27C0_67CB,
    ]
)

LARGEST = Scalar(
    [
        0xFFFF_FFFF_0000_0000,
        0x53BD_A402_FFFE_5BFE,
        0x3339_D808_09A1_D805,
        0x73ED_A753_299D_7D48,
    ]
)

ONE = Scalar(
    [8589934590, 6378425256633387010, 11064306276430008309, 1739710354780652911]
)
