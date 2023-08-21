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


class TestFp(unittest.TestCase):
    def test_zero(self):
        zero = Fp6.zero()
        self.assertTrue(
            zero.c0.eq(Fp2.zero()) and zero.c1.eq(Fp2.zero()) and zero.c2.eq(Fp2.zero())
        )

    def test_one(self):
        one = Fp6.one()
        self.assertTrue(
            one.c0.eq(Fp2.one()) and one.c1.eq(Fp2.zero()) and one.c2.eq(Fp2.zero())
        )

    def test_default(self):
        self.assertTrue(Fp6.default().eq(Fp6.zero()))


if __name__ == "__main__":
    unittest.main()
