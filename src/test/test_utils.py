import unittest
from src.utils import (
    sbb,
)


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


if __name__ == "__main__":
    unittest.main()
