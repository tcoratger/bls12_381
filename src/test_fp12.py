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
import random
from src.utils import array_to_number


class TestFp(unittest.TestCase):
    def test_from_fp(self):
        a = Fp.random(random.Random())
        b = Fp12.from_fp(a)
        self.assertTrue(b.c0.eq(Fp6.from_fp(a)) and b.c1.is_zero())

    def test_from_fp2(self):
        a = Fp2.random(random.Random())
        b = Fp12.from_fp2(a)
        self.assertTrue(b.c0.eq(Fp6.from_fp2(a)) and b.c1.is_zero())

    def test_from_fp6(self):
        a = Fp6.random(random.Random())
        b = Fp12.from_fp6(a)
        self.assertTrue(b.c0.eq(a) and b.c1.is_zero())
