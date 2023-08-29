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

    def from_u64(val):
        return Scalar([val, 0, 0, 0])

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
    def montgomery_reduce(t0, t1, t2, t3, t4, t5, t6, t7):
        # The Montgomery reduction here is based on Algorithm 14.32 in
        # Handbook of Applied Cryptography
        # <http://cacr.uwaterloo.ca/hac/about/chap14.pdf>.

        k = wrapping_mul_u64(t0, INV)
        _, carry = mac(t0, k, MODULUS.array[0], 0)
        r1, carry = mac(t1, k, MODULUS.array[1], carry)
        r2, carry = mac(t2, k, MODULUS.array[2], carry)
        r3, carry = mac(t3, k, MODULUS.array[3], carry)
        r4, carry2 = adc(t4, 0, carry)

        k = wrapping_mul_u64(r1, INV)
        _, carry = mac(r1, k, MODULUS.array[0], 0)
        r2, carry = mac(r2, k, MODULUS.array[1], carry)
        r3, carry = mac(r3, k, MODULUS.array[2], carry)
        r4, carry = mac(r4, k, MODULUS.array[3], carry)
        r5, carry2 = adc(t5, carry2, carry)

        k = wrapping_mul_u64(r2, INV)
        _, carry = mac(r2, k, MODULUS.array[0], 0)
        r3, carry = mac(r3, k, MODULUS.array[1], carry)
        r4, carry = mac(r4, k, MODULUS.array[2], carry)
        r5, carry = mac(r5, k, MODULUS.array[3], carry)
        r6, carry2 = adc(t6, carry2, carry)

        k = wrapping_mul_u64(r3, INV)
        _, carry = mac(r3, k, MODULUS.array[0], 0)
        r4, carry = mac(r4, k, MODULUS.array[1], carry)
        r5, carry = mac(r5, k, MODULUS.array[2], carry)
        r6, carry = mac(r6, k, MODULUS.array[3], carry)
        r7, _ = adc(t7, carry2, carry)

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
