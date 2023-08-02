import unittest
from src.utils import sbb, mac


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


if __name__ == "__main__":
    unittest.main()
