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
