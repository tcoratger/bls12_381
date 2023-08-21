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
import random


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

    def test_from_fp(self):
        a = Fp(
            [
                0x1234_5678_90AB_CDEF,
                0x9876_5432_10FE_DCBA,
                0xAAAA_BBBB_CCCC_DDDD,
                0x1111_2222_3333_4444,
                0xCCCC_DDDD_EEEE_FFFF,
                0xFFFF_0000_1111_2222,
            ]
        )
        b = Fp6.from_fp(a)
        self.assertTrue(
            b.c0.eq(Fp2.from_fp(a)) and b.c1.eq(Fp2.zero()) and b.c2.eq(Fp2.zero())
        )

    def test_from_fp2(self):
        a = Fp2(
            Fp(
                [
                    0xC9A2_1831_63EE_70D4,
                    0xBC37_70A7_196B_5C91,
                    0xA247_F8C1_304C_5F44,
                    0xB01F_C2A3_726C_80B5,
                    0xE1D2_93E5_BBD9_19C9,
                    0x04B7_8E80_020E_F2CA,
                ]
            ),
            Fp(
                [
                    0x952E_A446_0462_618F,
                    0x238D_5EDD_F025_C62F,
                    0xF6C9_4B01_2EA9_2E72,
                    0x03CE_24EA_C1C9_3808,
                    0x0559_50F9_45DA_483C,
                    0x010A_768D_0DF4_EABC,
                ]
            ),
        )
        b = Fp6.from_fp2(a)
        self.assertTrue(b.c0.eq(a) and b.c1.eq(Fp2.zero()) and b.c2.eq(Fp2.zero()))

    def test_toto(self):



if __name__ == "__main__":
    unittest.main()
