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
