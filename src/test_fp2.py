import unittest
from src.fp import (
    Fp,
)
from src.fp2 import (
    Fp2,
)


class TestZero(unittest.TestCase):
    def test_is_zero(self):
        a = Fp2.zero()
        self.assertTrue(a.c0.eq(Fp.zero()) and a.c1.eq(Fp.zero()))


class TestOne(unittest.TestCase):
    def test_one(self):
        a = Fp2.one()
        self.assertTrue(a.c0.eq(Fp.one()) and a.c1.eq(Fp.zero()))


class TestEq(unittest.TestCase):
    def test_eq(self):
        a = Fp(
            [
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
            ]
        )
        b = Fp(
            [
                0xB9FEFFFFFFFFAAAC,
                0x1EABFFFEB153FFFF,
                0x6730D2A0F6B0F624,
                0x64774B84F38512BF,
                0x4B1BA7B6434BACD7,
                0x1A0111EA397FE69A,
            ]
        )
        c = Fp2(a, b)
        self.assertTrue(c.eq(c))


class TestDefault(unittest.TestCase):
    def test_default(self):
        a = Fp2.default()
        self.assertTrue(a.c0.eq(Fp.zero()) and a.c1.eq(Fp.zero()))


class TestIsZero(unittest.TestCase):
    def test_is_zero(self):
        a = Fp2.zero()
        self.assertTrue(a.is_zero())


class TestConjugate(unittest.TestCase):
    def test_conjugate(self):
        a = Fp(
            [
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
            ]
        )
        b = Fp(
            [
                0xB9FEFFFFFFFFAAAC,
                0x1EABFFFEB153FFFF,
                0x6730D2A0F6B0F624,
                0x64774B84F38512BF,
                0x4B1BA7B6434BACD7,
                0x1A0111EA397FE69A,
            ]
        )
        c = Fp2(a, b)
        d = c.conjugate()
        self.assertTrue(d.c0.eq(c.c0) and d.c1.eq(-(c.c1)))

    def test_conjugate_zero(self):
        a = Fp2(Fp.zero(), Fp.zero())
        b = a.conjugate()
        self.assertTrue(b.c0.eq(Fp.zero()) and b.c1.eq(Fp.zero()))


class TestMulByNonResidue(unittest.TestCase):
    def test_mul_by_nonresidue(self):
        a = Fp(
            [
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
                0xFFFFFFFF_FFFFFFFF,
            ]
        )
        b = Fp(
            [
                0xB9FEFFFFFFFFAAAC,
                0x1EABFFFEB153FFFF,
                0x6730D2A0F6B0F624,
                0x64774B84F38512BF,
                0x4B1BA7B6434BACD7,
                0x1A0111EA397FE69A,
            ]
        )
        c = Fp2(a, b)
        d = c.mul_by_nonresidue()
        self.assertTrue(d.c0.eq(a - b) and d.c1.eq(a + b))


class TestLexicographicLargest(unittest.TestCase):
    def test_lexicographic_largest(self):
        self.assertFalse(Fp2.zero().lexicographically_largest())
        self.assertFalse(Fp2.one().lexicographically_largest())
        self.assertTrue(
            Fp2(
                Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp(
                    [
                        0xD328_E37C_C2F5_8D41,
                        0x948D_F085_8A60_5869,
                        0x6032_F9D5_6F93_A573,
                        0x2BE4_83EF_3FFF_DC87,
                        0x30EF_61F8_8F48_3C2A,
                        0x1333_F55A_3572_5BE0,
                    ]
                ),
            ).lexicographically_largest()
        )
        self.assertFalse(
            Fp2(
                -Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                -Fp(
                    [
                        0xD328_E37C_C2F5_8D41,
                        0x948D_F085_8A60_5869,
                        0x6032_F9D5_6F93_A573,
                        0x2BE4_83EF_3FFF_DC87,
                        0x30EF_61F8_8F48_3C2A,
                        0x1333_F55A_3572_5BE0,
                    ]
                ),
            ).lexicographically_largest()
        )
        self.assertFalse(
            Fp2(
                Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp.zero(),
            ).lexicographically_largest()
        )
        self.assertTrue(
            Fp2(
                -Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp.zero(),
            ).lexicographically_largest()
        )
