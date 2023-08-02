import unittest
from src.utils import sbb, mac, adc, wrapping_mul_u64


class TestSbb(unittest.TestCase):
    # Test cases with no underflow
    def test_no_underflow(self):
        self.assertEqual(
            sbb(0x23456789ABCDEF12, 0x123456789ABCDEF0, 0x1),
            (0x1111111111111022, 0x0),
        )
        self.assertEqual(
            sbb(0x23456789ABCDEF12, 0x123456789ABCDEF0, 0x0),
            (0x1111111111111022, 0x0),
        )

    # Test cases with underflow
    def test_underflow(self):
        self.assertEqual(
            sbb(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x0),
            (0xEEEEEEEEEEEEEFDE, 0xFFFFFFFFFFFFFFFF),
        )
        self.assertEqual(
            sbb(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x1),
            (0xEEEEEEEEEEEEEFDE, 0xFFFFFFFFFFFFFFFF),
        )

    # Test case with both inputs being zero
    def test_zero(self):
        self.assertEqual(
            sbb(0x0, 0x0, 0x1),
            (0x0, 0x0),
        )

    # Test case with no borrow (inputs are equal)
    def test_no_borrow(self):
        self.assertEqual(
            sbb(0x1111111111111111, 0x1111111111111111, 0x0),
            (0x0, 0x0),
        )


class TestMac(unittest.TestCase):
    # Test cases with no carry
    def test_no_carry(self):
        self.assertEqual(
            mac(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x3456789ABCDEF012, 0x0),
            (0x5BB3283248F48E34, 0x73602F699740C64),
        )
        self.assertEqual(
            mac(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0x0),
            (0x0, 0xFFFFFFFFFFFFFFFF),
        )

    # Test cases with carry
    def test_with_carry(self):
        self.assertEqual(
            mac(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x3456789ABCDEF012, 0x1),
            (0x5BB3283248F48E35, 0x73602F699740C64),
        )
        self.assertEqual(
            mac(
                0x1111111111111111,
                0x1111111111111111,
                0x1111111111111111,
                0xFFFFFFFFFFFFFFFF,
            ),
            (0x20FEDCBA98765431, 0x123456789ABCDF1),
        )

    # Test case with zero input
    def test_zero_input(self):
        self.assertEqual(
            mac(0x0, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0x0),
            (0x1, 0xFFFFFFFFFFFFFFFE),
        )
        self.assertEqual(
            mac(0x0, 0x0, 0x0, 0x0),
            (0x0, 0x0),
        )


class TestAdc(unittest.TestCase):
    # Test cases with no carry
    def test_no_carry(self):
        self.assertEqual(
            adc(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x0),
            (0x3579BE02468ACE02, 0x0),
        )
        self.assertEqual(
            adc(0xFFFFFFFFFFFFFFFF, 0x1, 0x0),
            (0x0, 0x1),
        )

    # Test cases with carry
    def test_with_carry(self):
        self.assertEqual(
            adc(0x123456789ABCDEF0, 0x23456789ABCDEF12, 0x1),
            (0x3579BE02468ACE03, 0x0),
        )
        self.assertEqual(
            adc(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF),
            (0xFFFFFFFFFFFFFFFD, 0x2),
        )

    # Test case with zero input
    def test_zero_input(self):
        self.assertEqual(
            adc(0x0, 0x0, 0x0),
            (0x0, 0x0),
        )
        self.assertEqual(
            adc(0x0, 0xFFFFFFFFFFFFFFFF, 0x0),
            (0xFFFFFFFFFFFFFFFF, 0x0),
        )


class TestWrappingMulU64(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(wrapping_mul_u64(10, 20), 200)
        self.assertEqual(wrapping_mul_u64(2**32, 2**32), 0)
        self.assertEqual(wrapping_mul_u64(2**63 - 1, 2), 2**64 - 2)

    def test_zero(self):
        self.assertEqual(wrapping_mul_u64(0, 1234), 0)
        self.assertEqual(wrapping_mul_u64(9876, 0), 0)

    def test_overflow(self):
        self.assertEqual(wrapping_mul_u64(2**63, 2**63), 0)
        self.assertEqual(wrapping_mul_u64(2**64 - 1, 2**64 - 1), 1)

    def test_large_numbers(self):
        self.assertEqual(
            wrapping_mul_u64(2**62 - 1, 2**62 - 1), 9223372036854775809
        )
        self.assertEqual(
            wrapping_mul_u64(1234567890123456, 9876543210987654), 3007213678458421376
        )


if __name__ == "__main__":
    unittest.main()
