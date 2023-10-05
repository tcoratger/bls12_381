from src.fp import Fp
from src.fp2 import Fp2
from src.fp6 import Fp6
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
from src.fp12 import (
    Fp12,
)
from src.g1 import G1Affine
from src.g2 import G2Affine, G2Projective
from abc import ABC, abstractmethod


class MillerLoopDriver(ABC):
    @abstractmethod
    def doubling_step(self, f):
        pass

    @abstractmethod
    def addition_step(self, f):
        pass

    @abstractmethod
    def square_output(self, f):
        pass

    @abstractmethod
    def conjugate(self, f):
        pass

    @abstractmethod
    def one(self):
        pass


# Represents results of a Miller loop, one of the most expensive portions
# of the pairing function. `MillerLoopResult`s cannot be compared with each
# other until `.final_exponentiation()` is called, which is also expensive.
class MillerLoopResult:
    def __init__(self, fp: Fp12):
        self.fp = fp

    def __add__(self, rhs):
        return self.add(rhs)

    def default():
        return MillerLoopResult(Fp12.one())

    def conditional_select(a, b, choice: Choice):
        return MillerLoopResult(Fp12.conditional_select(a.fp, b.fp, choice))

    def add(self, rhs):
        return MillerLoopResult(self.fp * rhs.fp)

    def fp4_square(a: Fp2, b: Fp2):
        t0 = a.square()
        t1 = b.square()
        t2 = t1.mul_by_nonresidue()
        c0 = t2 + t0
        t2 = a + b
        t2 = t2.square()
        t2 -= t0
        c1 = t2 - t1

        return (c0, c1)

    # Adaptation of Algorithm 5.5.4, Guide to Pairing-Based Cryptography
    # Faster Squaring in the Cyclotomic Subgroup of Sixth Degree Extensions
    # https://eprint.iacr.org/2009/565.pdf
    def cyclotomic_square(f: Fp12):
        z0 = f.c0.c0
        z4 = f.c0.c1
        z3 = f.c0.c2
        z2 = f.c1.c0
        z1 = f.c1.c1
        z5 = f.c1.c2

        (t0, t1) = MillerLoopResult.fp4_square(z0, z1)

        # For A
        z0 = t0 - z0
        z0 = z0 + z0 + t0

        z1 = t1 + z1
        z1 = z1 + z1 + t1

        (t0, t1) = MillerLoopResult.fp4_square(z2, z3)
        (t2, t3) = MillerLoopResult.fp4_square(z4, z5)

        # For C
        z4 = t0 - z4
        z4 = z4 + z4 + t0

        z5 = t1 + z5
        z5 = z5 + z5 + t1

        # For B
        t0 = t3.mul_by_nonresidue()
        z2 = t0 + z2
        z2 = z2 + z2 + t0

        z3 = t2 - z3
        z3 = z3 + z3 + t2

        return Fp12(
            Fp6(
                z0,
                z4,
                z3,
            ),
            Fp6(
                z2,
                z1,
                z5,
            ),
        )

    def cyclotomic_exp(f: Fp12):
        x = BLS_X
        tmp = Fp12.one()
        found_one = False

        for b in reversed([(x >> b) & 1 for b in range(64)]):
            if found_one:
                tmp = MillerLoopResult.cyclotomic_square(tmp)
            else:
                found_one = b

            if b:
                tmp *= f

        return tmp.conjugate()

    def final_exponentiation(self):
        f = self.fp
        t0 = (
            f.frobenius_map()
            .frobenius_map()
            .frobenius_map()
            .frobenius_map()
            .frobenius_map()
            .frobenius_map()
        )

        a = Fp12.invert(f)

        if a.choice:
            t1 = a.value
            t2 = t0 * t1
            t1 = t2
            t2 = t2.frobenius_map().frobenius_map()
            t2 *= t1
            t1 = MillerLoopResult.cyclotomic_square(t2).conjugate()
            t3 = MillerLoopResult.cyclotomic_exp(t2)
            t4 = MillerLoopResult.cyclotomic_square(t3)
            t5 = t1 * t3
            t1 = MillerLoopResult.cyclotomic_exp(t5)
            t0 = MillerLoopResult.cyclotomic_exp(t1)
            t6 = MillerLoopResult.cyclotomic_exp(t0)
            t6 *= t4
            t4 = MillerLoopResult.cyclotomic_exp(t6)
            t5 = t5.conjugate()
            t4 *= t5 * t2
            t5 = t2.conjugate()
            t1 *= t2
            t1 = t1.frobenius_map().frobenius_map().frobenius_map()
            t6 *= t5
            t6 = t6.frobenius_map()
            t3 *= t0
            t3 = t3.frobenius_map().frobenius_map()
            t3 *= t1
            t3 *= t6
            f = t3 * t4
            return Gt(f)

        # We unwrap() because `MillerLoopResult` can only be constructed
        # by a function within this crate, and we uphold the invariant
        # that the enclosed value is nonzero.
        raise ValueError(
            "Error: Cannot compute final exponentiation with t1.choice = False"
        )


# This is an element of $\mathbb{G}_T$, the target group of the pairing function. As with
# $\mathbb{G}_1$ and $\mathbb{G}_2$ this group has order $q$.
#
# Typically, $\mathbb{G}_T$ is written multiplicatively but we will write it additively to
# keep code and abstractions consistent.
class Gt:
    def __init__(self, fp: Fp12):
        self.fp = fp

    def __neg__(self):
        return self.neg()

    def __add__(self, rhs):
        return self.add(rhs)

    def __sub__(self, other):
        return self.sub(other)

    def __str__(self):
        result = f"Gt({self.fp})\n"
        return result

    def __mul__(lhs, rhs):
        if isinstance(rhs, Scalar):
            return lhs.mul(rhs)
        else:
            raise ValueError("Unsupported type for multiplication")

    def mul(self, other: Scalar):
        acc = Gt.identity()

        # This is a simple double-and-add implementation of group element
        # multiplication, moving from most significant to least
        # significant bit of the scalar.
        #
        # We skip the leading bit because it's always unset for Fq
        # elements.
        for byte in reversed(other.to_bytes()):
            for i in range(7, -1, -1):
                bit = Choice(1) if (byte >> i) & 1 else Choice(0)
                acc = acc.double()
                acc = Gt.conditional_select(acc, acc + self, bit)

        return acc

    # Returns the group identity, which is $1$.
    @staticmethod
    def identity():
        return Gt(Fp12.one())

    def is_identity(self):
        return self.eq(Gt.identity())

    @staticmethod
    def default():
        return Gt.identity()

    def eq(self, other):
        return self.fp.eq(other.fp)

    def conditional_select(a, b, choice: Choice):
        return Gt(Fp12.conditional_select(a.fp, b.fp, choice))

    # Doubles this group element.
    def double(self):
        return Gt(self.fp.square())

    def neg(self):
        # The element is unitary, so we just conjugate.
        return Gt(self.fp.conjugate())

    def add(self, rhs):
        return Gt(self.fp * rhs.fp)

    def sub(self, rhs):
        return self + (-rhs)

    def generator():
        # pairing(&G1Affine::generator(), &G2Affine::generator())
        return Gt(
            Fp12(
                Fp6(
                    Fp2(
                        Fp(
                            [
                                0x1972_E433_A01F_85C5,
                                0x97D3_2B76_FD77_2538,
                                0xC8CE_546F_C96B_CDF9,
                                0xCEF6_3E73_66D4_0614,
                                0xA611_3427_8184_3780,
                                0x13F3_448A_3FC6_D825,
                            ]
                        ),
                        Fp(
                            [
                                0xD263_31B0_2E9D_6995,
                                0x9D68_A482_F779_7E7D,
                                0x9C9B_2924_8D39_EA92,
                                0xF480_1CA2_E131_07AA,
                                0xA16C_0732_BDBC_B066,
                                0x083C_A4AF_BA36_0478,
                            ]
                        ),
                    ),
                    Fp2(
                        Fp(
                            [
                                0x59E2_61DB_0916_B641,
                                0x2716_B6F4_B23E_960D,
                                0xC8E5_5B10_A0BD_9C45,
                                0x0BDB_0BD9_9C4D_EDA8,
                                0x8CF8_9EBF_57FD_AAC5,
                                0x12D6_B792_9E77_7A5E,
                            ]
                        ),
                        Fp(
                            [
                                0x5FC8_5188_B0E1_5F35,
                                0x34A0_6E3A_8F09_6365,
                                0xDB31_26A6_E02A_D62C,
                                0xFC6F_5AA9_7D9A_990B,
                                0xA12F_55F5_EB89_C210,
                                0x1723_703A_926F_8889,
                            ]
                        ),
                    ),
                    Fp2(
                        Fp(
                            [
                                0x9358_8F29_7182_8778,
                                0x43F6_5B86_11AB_7585,
                                0x3183_AAF5_EC27_9FDF,
                                0xFA73_D7E1_8AC9_9DF6,
                                0x64E1_76A6_A64C_99B0,
                                0x179F_A78C_5838_8F1F,
                            ]
                        ),
                        Fp(
                            [
                                0x672A_0A11_CA2A_EF12,
                                0x0D11_B9B5_2AA3_F16B,
                                0xA444_12D0_699D_056E,
                                0xC01D_0177_221A_5BA5,
                                0x66E0_CEDE_6C73_5529,
                                0x05F5_A71E_9FDD_C339,
                            ]
                        ),
                    ),
                ),
                Fp6(
                    Fp2(
                        Fp(
                            [
                                0xD30A_88A1_B062_C679,
                                0x5AC5_6A5D_35FC_8304,
                                0xD0C8_34A6_A81F_290D,
                                0xCD54_30C2_DA37_07C7,
                                0xF0C2_7FF7_8050_0AF0,
                                0x0924_5DA6_E2D7_2EAE,
                            ]
                        ),
                        Fp(
                            [
                                0x9F2E_0676_791B_5156,
                                0xE2D1_C823_4918_FE13,
                                0x4C9E_459F_3C56_1BF4,
                                0xA3E8_5E53_B9D3_E3C1,
                                0x820A_121E_21A7_0020,
                                0x15AF_6183_41C5_9ACC,
                            ]
                        ),
                    ),
                    Fp2(
                        Fp(
                            [
                                0x7C95_658C_2499_3AB1,
                                0x73EB_3872_1CA8_86B9,
                                0x5256_D749_4774_34BC,
                                0x8BA4_1902_EA50_4A8B,
                                0x04A3_D3F8_0C86_CE6D,
                                0x18A6_4A87_FB68_6EAA,
                            ]
                        ),
                        Fp(
                            [
                                0xBB83_E71B_B920_CF26,
                                0x2A52_77AC_92A7_3945,
                                0xFC0E_E59F_94F0_46A0,
                                0x7158_CDF3_7860_58F7,
                                0x7CC1_061B_82F9_45F6,
                                0x03F8_47AA_9FDB_E567,
                            ]
                        ),
                    ),
                    Fp2(
                        Fp(
                            [
                                0x8078_DBA5_6134_E657,
                                0x1CD7_EC9A_4399_8A6E,
                                0xB1AA_599A_1A99_3766,
                                0xC9A0_F62F_0842_EE44,
                                0x8E15_9BE3_B605_DFFA,
                                0x0C86_BA0D_4AF1_3FC2,
                            ]
                        ),
                        Fp(
                            [
                                0xE80F_F2A0_6A52_FFB1,
                                0x7694_CA48_721A_906C,
                                0x7583_183E_03B0_8514,
                                0xF567_AFDD_40CE_E4E2,
                                0x9A6D_96D2_E526_A5FC,
                                0x197E_9F49_861F_2242,
                            ]
                        ),
                    ),
                ),
            )
        )


class AdderG2Prepared(MillerLoopDriver):
    def __init__(self, cur: G2Projective, base: G2Affine, coeffs: [(Fp2, Fp2, Fp2)]):
        self.cur = cur
        self.base = base
        self.coeffs = coeffs

    def doubling_step(self, _):
        coeffs = doubling_step(self.cur)
        self.coeffs.append(coeffs)

    def addition_step(self, _):
        coeffs = addition_step(self.cur, self.base)
        self.coeffs.append(coeffs)

    def square_output(self, _):
        pass

    def conjugate(self, _):
        pass

    def one(self):
        return ()


class G2Prepared:
    def __init__(self, infinity: Choice, coeffs: [Fp2, Fp2, Fp2]):
        self.infinity = infinity
        self.coeffs = coeffs

    def from_g2_affine(q: G2Affine):
        is_identity = q.is_identity()
        q = G2Affine.conditional_select(
            q, G2Affine.generator(), Choice(1) if is_identity else Choice(0)
        )
        adder = AdderG2Prepared(G2Projective.from_g2_affine(q), q, [])

        miller_loop(adder)

        assert len(adder.coeffs) == 68

        return G2Prepared(is_identity, adder.coeffs)


def ell(f: Fp12, coeffs: (Fp2, Fp2, Fp2), p: G1Affine):
    c0 = coeffs[0]
    c1 = coeffs[1]

    c0.c0 *= p.y
    c0.c1 *= p.y

    c1.c0 *= p.x
    c1.c1 *= p.x

    return f.mul_by_014(coeffs[2], c1, c0)


def doubling_step(r: G2Projective):
    # Adaptation of Algorithm 26, https://eprint.iacr.org/2010/354.pdf
    tmp0 = r.x.square()
    tmp1 = r.y.square()
    tmp2 = tmp1.square()
    tmp3 = (tmp1 + r.x).square() - tmp0 - tmp2
    tmp3 = tmp3 + tmp3
    tmp4 = tmp0 + tmp0 + tmp0
    tmp6 = r.x + tmp4
    tmp5 = tmp4.square()
    zsquared = r.z.square()
    r.x = tmp5 - tmp3 - tmp3
    r.z = (r.z + r.y).square() - tmp1 - zsquared
    r.y = (tmp3 - r.x) * tmp4
    tmp2 = tmp2 + tmp2
    tmp2 = tmp2 + tmp2
    tmp2 = tmp2 + tmp2
    r.y -= tmp2
    tmp3 = tmp4 * zsquared
    tmp3 = tmp3 + tmp3
    tmp3 = -tmp3
    tmp6 = tmp6.square() - tmp0 - tmp5
    tmp1 = tmp1 + tmp1
    tmp1 = tmp1 + tmp1
    tmp6 = tmp6 - tmp1
    tmp0 = r.z * zsquared
    tmp0 = tmp0 + tmp0

    return (tmp0, tmp3, tmp6)


def addition_step(r: G2Projective, q: G2Affine):
    # Adaptation of Algorithm 27, https://eprint.iacr.org/2010/354.pdf
    zsquared = r.z.square()
    ysquared = q.y.square()
    t0 = zsquared * q.x
    t1 = ((q.y + r.z).square() - ysquared - zsquared) * zsquared
    t2 = t0 - r.x
    t3 = t2.square()
    t4 = t3 + t3
    t4 = t4 + t4
    t5 = t4 * t2
    t6 = t1 - r.y - r.y
    t9 = t6 * q.x
    t7 = t4 * r.x
    r.x = t6.square() - t5 - t7 - t7
    r.z = (r.z + t2).square() - zsquared - t3
    t10 = q.y + r.z
    t8 = (t7 - r.x) * t6
    t0 = r.y * t5
    t0 = t0 + t0
    r.y = t8 - t0
    t10 = t10.square() - ysquared
    ztsquared = r.z.square()
    t10 = t10 - ztsquared
    t9 = t9 + t9 - t10
    t10 = r.z + r.z
    t6 = -t6
    t1 = t6 + t6

    return (t10, t1, t9)


class Adder(MillerLoopDriver):
    def __init__(self, cur: G2Projective, base: G2Affine, p: G1Affine):
        self.cur = cur
        self.base = base
        self.p = p

    def doubling_step(self, f: Fp12):
        coeffs = doubling_step(self.cur)
        return ell(f, coeffs, self.p)

    def addition_step(self, f: Fp12):
        coeffs = addition_step(self.cur, self.base)
        return ell(f, coeffs, self.p)

    def square_output(self, f: Fp12):
        return f.square()

    def conjugate(self, f: Fp12):
        return f.conjugate()

    def one(self):
        return Fp12.one()


class AdderMulti(MillerLoopDriver):
    def __init__(self, terms: [(G1Affine, G2Prepared)], index):
        self.terms = terms
        self.index = index

    def doubling_step(self, f):
        index = self.index
        for term in self.terms:
            either_identity = term[0].is_identity() or term[1].infinity

            new_f = ell(f, term[1].coeffs[index], term[0])
            f = Fp12.conditional_select(
                new_f, f, Choice(1) if either_identity else Choice(0)
            )

        self.index += 1
        return f

    def addition_step(self, f):
        index = self.index
        for term in self.terms:
            either_identity = term[0].is_identity() or term[1].infinity

            new_f = ell(f, term[1].coeffs[index], term[0])
            f = Fp12.conditional_select(
                new_f, f, Choice(1) if either_identity else Choice(0)
            )

        self.index += 1
        return f

    def square_output(self, f):
        return f.square()

    def conjugate(self, f):
        return f.conjugate()

    def one(self):
        return Fp12.one()


# This is a "generic" implementation of the Miller loop to avoid duplicating code
# structure elsewhere instead, we'll write concrete instantiations of
# `MillerLoopDriver` for whatever purposes we need (such as caching modes).
def miller_loop(driver: MillerLoopDriver):
    f = driver.one()

    found_one = False

    for b in [
        (((BLS_X >> 1) >> b & 1) & ((1 << 64) - 1)) == 1 for b in reversed(range(64))
    ]:
        if not found_one:
            found_one = b
            continue

        f = driver.doubling_step(f)

        if b:
            f = driver.addition_step(f)

        f = driver.square_output(f)

    f = driver.doubling_step(f)

    if BLS_X_IS_NEGATIVE:
        f = driver.conjugate(f)

    return f


# Computes $$\sum_{i=1}^n \textbf{ML}(a_i, b_i)$$ given a series of terms
# $$(a_1, b_1), (a_2, b_2), ..., (a_n, b_n).$$
#
# Requires the `alloc` and `pairing` crate features to be enabled.
def multi_miller_loop(terms: [(G1Affine, G2Prepared)]):
    adder = AdderMulti(terms, 0)
    tmp = miller_loop(adder)

    return MillerLoopResult(tmp)


def pairing(p: G1Affine, q: G2Affine):
    either_identity = p.is_identity().value == 1 or q.is_identity()
    p = G1Affine.conditional_select(
        p, G1Affine.generator(), Choice(1) if either_identity else Choice(0)
    )
    q = G2Affine.conditional_select(
        q, G2Affine.generator(), Choice(1) if either_identity else Choice(0)
    )

    adder = Adder(G2Projective.from_g2_affine(q), q, p)

    tmp = miller_loop(adder)
    tmp = MillerLoopResult(
        Fp12.conditional_select(
            tmp, Fp12.one(), Choice(1) if either_identity else Choice(0)
        )
    )

    return tmp.final_exponentiation()
