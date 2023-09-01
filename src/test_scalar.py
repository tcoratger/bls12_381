import unittest
from src.fp import (
    Fp,
)
from src.fp2 import (
    Fp2,
)
from src.fp6 import (
    Fp6,
)
from src.fp12 import (
    Fp12,
)
from src.scalar import (
    Scalar,
    MODULUS,
    TWO_INV,
    ROOT_OF_UNITY,
    R2,
    LARGEST,
    R,
    R3,
    ROOT_OF_UNITY_INV,
    ONE,
    INV,
    S,
    DELTA,
)
from src.g1 import G1Affine, G1Projective
import random
from src.utils import array_to_number, Choice, wrapping_mul_u64


class TestBasics(unittest.TestCase):
    def test_from_u64(self):
        a = Scalar.from_u64(10)
        self.assertTrue(a.eq(Scalar([10, 0, 0, 0]) * R2))

    def test_eq(self):
        a = Scalar([2, 4, 43, 17])
        self.assertTrue(a.eq(Scalar([2, 4, 43, 17])))

    def test_conditional_select(self):
        a = Scalar([2, 4, 43, 17])
        b = Scalar([45, 2, 4, 10])
        self.assertTrue(Scalar.conditional_select(a, b, Choice(0)).eq(a))
        self.assertTrue(Scalar.conditional_select(a, b, Choice(1)).eq(b))

    def test_zero(self):
        self.assertEqual(Scalar.zero().array, [0, 0, 0, 0])


class TestEquality(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(Scalar.zero().eq(Scalar.zero()))
        self.assertTrue(Scalar.one().eq(Scalar.one()))
        self.assertTrue(R2.eq(R2))
        self.assertFalse(Scalar.one().eq(Scalar.zero()))
        self.assertFalse(Scalar.one().eq(R2))


class TestZero(unittest.TestCase):
    def test_zero(self):
        self.assertTrue(Scalar.zero().eq(-Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() + Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() - Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() * Scalar.zero()))


class TestNegation(unittest.TestCase):
    def test_negation(self):
        tmp = -LARGEST
        self.assertTrue(tmp.eq(Scalar([1, 0, 0, 0])))

        tmp = -Scalar.zero()
        self.assertTrue(tmp.eq(Scalar.zero()))

        tmp = -Scalar([1, 0, 0, 0])
        self.assertTrue(tmp.eq(LARGEST))


class TestSubtraction(unittest.TestCase):
    def test_subtraction(self):
        tmp = LARGEST
        tmp -= LARGEST
        self.assertTrue(tmp.eq(Scalar.zero()))

        tmp = Scalar.zero()
        tmp -= LARGEST

        tmp2 = MODULUS
        tmp2 -= LARGEST
        self.assertTrue(tmp.eq(tmp2))


class TestToBytes(unittest.TestCase):
    def test_to_bytes(self):
        self.assertEqual(
            Scalar.zero().to_bytes(),
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
        )
        self.assertEqual(
            Scalar.one().to_bytes(),
            [
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
        )
        self.assertEqual(
            R2.to_bytes(),
            [
                254,
                255,
                255,
                255,
                1,
                0,
                0,
                0,
                2,
                72,
                3,
                0,
                250,
                183,
                132,
                88,
                245,
                79,
                188,
                236,
                239,
                79,
                140,
                153,
                111,
                5,
                197,
                172,
                89,
                177,
                36,
                24,
            ],
        )
        self.assertEqual(
            (-Scalar.one()).to_bytes(),
            [
                0,
                0,
                0,
                0,
                255,
                255,
                255,
                255,
                254,
                91,
                254,
                255,
                2,
                164,
                189,
                83,
                5,
                216,
                161,
                9,
                8,
                216,
                57,
                51,
                72,
                125,
                157,
                41,
                83,
                167,
                237,
                115,
            ],
        )


class TestFromBytes(unittest.TestCase):
    def test_from_bytes(self):
        self.assertTrue(
            Scalar.from_bytes(
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            ).value.eq(Scalar.zero())
        )
        self.assertTrue(
            Scalar.from_bytes(
                [
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            ).value.eq(Scalar.one())
        )
        self.assertTrue(
            Scalar.from_bytes(
                [
                    254,
                    255,
                    255,
                    255,
                    1,
                    0,
                    0,
                    0,
                    2,
                    72,
                    3,
                    0,
                    250,
                    183,
                    132,
                    88,
                    245,
                    79,
                    188,
                    236,
                    239,
                    79,
                    140,
                    153,
                    111,
                    5,
                    197,
                    172,
                    89,
                    177,
                    36,
                    24,
                ]
            ).value.eq(R2)
        )
        self.assertEqual(
            Scalar.from_bytes(
                [
                    0,
                    0,
                    0,
                    0,
                    255,
                    255,
                    255,
                    255,
                    254,
                    91,
                    254,
                    255,
                    2,
                    164,
                    189,
                    83,
                    5,
                    216,
                    161,
                    9,
                    8,
                    216,
                    57,
                    51,
                    72,
                    125,
                    157,
                    41,
                    83,
                    167,
                    237,
                    115,
                ]
            ).choice.value,
            Choice(1).value,
        )
        # modulus is invalid
        self.assertEqual(
            Scalar.from_bytes(
                [
                    1,
                    0,
                    0,
                    0,
                    255,
                    255,
                    255,
                    255,
                    254,
                    91,
                    254,
                    255,
                    2,
                    164,
                    189,
                    83,
                    5,
                    216,
                    161,
                    9,
                    8,
                    216,
                    57,
                    51,
                    72,
                    125,
                    157,
                    41,
                    83,
                    167,
                    237,
                    115,
                ]
            ).choice.value,
            Choice(0).value,
        )
        # Anything larger than the modulus is invalid
        self.assertEqual(
            Scalar.from_bytes(
                [
                    2,
                    0,
                    0,
                    0,
                    255,
                    255,
                    255,
                    255,
                    254,
                    91,
                    254,
                    255,
                    2,
                    164,
                    189,
                    83,
                    5,
                    216,
                    161,
                    9,
                    8,
                    216,
                    57,
                    51,
                    72,
                    125,
                    157,
                    41,
                    83,
                    167,
                    237,
                    115,
                ]
            ).choice.value,
            Choice(0).value,
        )
        self.assertEqual(
            Scalar.from_bytes(
                [
                    1,
                    0,
                    0,
                    0,
                    255,
                    255,
                    255,
                    255,
                    254,
                    91,
                    254,
                    255,
                    2,
                    164,
                    189,
                    83,
                    5,
                    216,
                    161,
                    9,
                    8,
                    216,
                    58,
                    51,
                    72,
                    125,
                    157,
                    41,
                    83,
                    167,
                    237,
                    115,
                ]
            ).choice.value,
            Choice(0).value,
        )
        self.assertEqual(
            Scalar.from_bytes(
                [
                    1,
                    0,
                    0,
                    0,
                    255,
                    255,
                    255,
                    255,
                    254,
                    91,
                    254,
                    255,
                    2,
                    164,
                    189,
                    83,
                    5,
                    216,
                    161,
                    9,
                    8,
                    216,
                    57,
                    51,
                    72,
                    125,
                    157,
                    41,
                    83,
                    167,
                    237,
                    116,
                ]
            ).choice.value,
            Choice(0).value,
        )


class TestFromU512(unittest.TestCase):
    def test_from_u512_zero(self):
        self.assertTrue(
            Scalar.zero().eq(
                Scalar.from_u512(
                    [
                        MODULUS.array[0],
                        MODULUS.array[1],
                        MODULUS.array[2],
                        MODULUS.array[3],
                        0,
                        0,
                        0,
                        0,
                    ]
                )
            )
        )

    def test_from_u512_r(self):
        self.assertTrue(R.eq(Scalar.from_u512([1, 0, 0, 0, 0, 0, 0, 0])))

    def test_from_u512_r2(self):
        self.assertTrue(R2.eq(Scalar.from_u512([0, 0, 0, 0, 1, 0, 0, 0])))

    def test_from_u512_max(self):
        max_u64 = 0xFFFF_FFFF_FFFF_FFFF
        self.assertTrue(
            (R3 - R).eq(
                Scalar.from_u512(
                    [
                        max_u64,
                        max_u64,
                        max_u64,
                        max_u64,
                        max_u64,
                        max_u64,
                        max_u64,
                        max_u64,
                    ]
                )
            )
        )


class TestFromBytesWide(unittest.TestCase):
    def test_from_bytes_wide_r2(self):
        self.assertTrue(
            R2.eq(
                Scalar.from_bytes_wide(
                    [
                        254,
                        255,
                        255,
                        255,
                        1,
                        0,
                        0,
                        0,
                        2,
                        72,
                        3,
                        0,
                        250,
                        183,
                        132,
                        88,
                        245,
                        79,
                        188,
                        236,
                        239,
                        79,
                        140,
                        153,
                        111,
                        5,
                        197,
                        172,
                        89,
                        177,
                        36,
                        24,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                    ]
                )
            )
        )

    def test_from_bytes_wide_negative_one(self):
        self.assertTrue(
            (-Scalar.one()).eq(
                Scalar.from_bytes_wide(
                    [
                        0,
                        0,
                        0,
                        0,
                        255,
                        255,
                        255,
                        255,
                        254,
                        91,
                        254,
                        255,
                        2,
                        164,
                        189,
                        83,
                        5,
                        216,
                        161,
                        9,
                        8,
                        216,
                        57,
                        51,
                        72,
                        125,
                        157,
                        41,
                        83,
                        167,
                        237,
                        115,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                    ]
                )
            )
        )

    def test_from_bytes_wide_maximum(self):
        self.assertTrue(
            Scalar(
                [
                    0xC62C_1805_439B_73B1,
                    0xC2B9_551E_8CED_218E,
                    0xDA44_EC81_DAF9_A422,
                    0x5605_AA60_1C16_2E79,
                ]
            ).eq(Scalar.from_bytes_wide([0xFF for _ in range(64)]))
        )


class TestAddition(unittest.TestCase):
    def test_addition(self):
        tmp = LARGEST
        tmp += LARGEST
        self.assertTrue(
            tmp.eq(
                Scalar(
                    [
                        0xFFFF_FFFE_FFFF_FFFF,
                        0x53BD_A402_FFFE_5BFE,
                        0x3339_D808_09A1_D805,
                        0x73ED_A753_299D_7D48,
                    ]
                )
            )
        )

        tmp = LARGEST
        tmp += Scalar([1, 0, 0, 0])
        self.assertTrue(tmp.eq(Scalar.zero()))


class TestMultiplication(unittest.TestCase):
    def test_multiplication(self):
        cur = LARGEST

        for _ in range(100):
            tmp = cur
            tmp *= cur

            tmp2 = Scalar.zero()
            for byte in reversed(cur.to_bytes()):
                for i in range(7, -1, -1):
                    b = (byte >> i) & (1 & 0xFF) == (1 & 0xFF)

                    tmp3 = tmp2
                    tmp2 += tmp3

                    if b:
                        tmp2 += cur

            self.assertTrue(tmp.eq(tmp2))

            cur += LARGEST


class TestSquaring(unittest.TestCase):
    def test_squaring(self):
        cur = LARGEST

        for _ in range(100):
            tmp = cur
            tmp = tmp.square()

            tmp2 = Scalar.zero()
            for byte in reversed(cur.to_bytes()):
                for i in range(7, -1, -1):
                    b = (byte >> i) & (1 & 0xFF) == (1 & 0xFF)

                    tmp3 = tmp2
                    tmp2 += tmp3

                    if b:
                        tmp2 += cur

            self.assertTrue(tmp.eq(tmp2))

            cur += LARGEST


class TestInversion(unittest.TestCase):
    def test_inversion(self):
        self.assertEqual(Scalar.zero().invert().choice.value, Choice(0).value)
        self.assertTrue(Scalar.one().invert().value.eq(Scalar.one()))
        self.assertTrue((-Scalar.one()).invert().value.eq(-Scalar.one()))

        tmp = R2

        for _ in range(100):
            tmp2 = tmp.invert().value
            tmp2 *= tmp

            self.assertTrue(tmp2.eq(Scalar.one()))

            tmp += R2


class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(
            array_to_number(MODULUS.array)
            == 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
        )
        self.assertTrue((Scalar.from_u64(2) * TWO_INV).eq(ONE))
        self.assertTrue((ROOT_OF_UNITY * ROOT_OF_UNITY_INV).eq(ONE))
        # ROOT_OF_UNITY^{2^s} mod m == 1
        self.assertTrue(ROOT_OF_UNITY.pow([1 << S, 0, 0, 0]).eq(ONE))
        # DELTA^{t} mod m == 1
        self.assertTrue(
            DELTA.pow(
                [
                    0xFFFE_5BFE_FFFF_FFFF,
                    0x09A1_D805_53BD_A402,
                    0x299D_7D48_3339_D808,
                    0x0000_0000_73ED_A753,
                ]
            ).eq(ONE)
        )
