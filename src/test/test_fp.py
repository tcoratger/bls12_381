import unittest
from src.fp import (
    Fp,
)


class TestFp(unittest.TestCase):
    def test_is_zero(self):
        self.assertTrue(Fp.zero().is_zero())
        self.assertFalse(
            Fp(
                [
                    0x1234_5678_90AB_CDEF,
                    0x9876_5432_10FE_DCBA,
                    0xAAAA_BBBB_CCCC_DDDD,
                    0x1111_2222_3333_4444,
                    0xCCCC_DDDD_EEEE_FFFF,
                    0xFFFF_0000_1111_2222,
                ]
            ).is_zero()
        )

    def test_eq(self):
        fp1 = Fp([1, 2, 3, 4, 5, 6])
        fp2 = Fp([1, 2, 3, 4, 5, 6])
        fp3 = Fp([6, 5, 4, 3, 2, 1])

        self.assertTrue(fp1.eq(fp2))
        self.assertFalse(fp1.eq(fp3))

    def test_neq(self):
        fp1 = Fp([1, 2, 3, 4, 5, 6])
        fp2 = Fp([1, 2, 3, 4, 5, 6])
        fp3 = Fp([6, 5, 4, 3, 2, 1])

        self.assertFalse(fp1.neq(fp2))
        self.assertTrue(fp1.neq(fp3))


if __name__ == "__main__":
    unittest.main()
