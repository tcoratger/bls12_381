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


class TestMontgomeryReduce(unittest.TestCase):
    # Test Montgomery Reduction
    def test_montgomery_reduce(self):
        # Test case 1
        t_values = [
            0x123456789ABCDEF0,
            0x23456789ABCDEF12,
            0x3456789ABCDEF012,
            0x456789ABCDEF0123,
            0x56789ABCDEF01234,
            0x6789ABCDEF012345,
            0x789ABCDEF0123456,
            0x89ABCDEF01234567,
            0x9ABCDEF012345678,
            0xABCDEF0123456789,
            0xBCDEF0123456789A,
            0xCDEF0123456789AB,
        ]
        expected_result = Fp(
            [
                0x5673FE9883899801,
                0x241B007C73824AD7,
                0xE1D2BCF78ED303CE,
                0x51F80197E26990D5,
                0x52EA28D5C1C0DC6,
                0xC80DAFCB56779679,
            ]
        )
        self.assertEqual(Fp.montgomery_reduce(*t_values).array, expected_result.array)

        # Test case 2
        t_values = [
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFF,
        ]

        expected_result = Fp(
            [
                0xC52B7DA6C7F4628B,
                0x9ECAED89D8BB0503,
                0x32F22927E21B885B,
                0x4CDFA0709ADC84D6,
                0x5DBD438F06FC594C,
                0x5024AE85084D9B0,
            ]
        )
        self.assertEqual(Fp.montgomery_reduce(*t_values).array, expected_result.array)


if __name__ == "__main__":
    unittest.main()
