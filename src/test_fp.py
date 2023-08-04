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


class TestFpEq(unittest.TestCase):
    def test_eq(self):
        fp1 = Fp([1, 2, 3, 4, 5, 6])

        self.assertTrue(fp1.eq(fp1))
        self.assertFalse(fp1.eq(Fp([7, 2, 3, 4, 5, 6])))
        self.assertFalse(fp1.eq(Fp([1, 7, 3, 4, 5, 6])))
        self.assertFalse(fp1.eq(Fp([1, 2, 7, 4, 5, 6])))
        self.assertFalse(fp1.eq(Fp([1, 2, 3, 7, 5, 6])))
        self.assertFalse(fp1.eq(Fp([1, 2, 3, 4, 7, 6])))
        self.assertFalse(fp1.eq(Fp([1, 2, 3, 4, 5, 7])))


class TestFpNeq(unittest.TestCase):
    def test_neq(self):
        fp1 = Fp([1, 2, 3, 4, 5, 6])

        self.assertFalse(fp1.neq(fp1))
        self.assertTrue(fp1.neq(Fp([7, 2, 3, 4, 5, 6])))
        self.assertTrue(fp1.neq(Fp([1, 7, 3, 4, 5, 6])))
        self.assertTrue(fp1.neq(Fp([1, 2, 7, 4, 5, 6])))
        self.assertTrue(fp1.neq(Fp([1, 2, 3, 7, 5, 6])))
        self.assertTrue(fp1.neq(Fp([1, 2, 3, 4, 7, 6])))
        self.assertTrue(fp1.neq(Fp([1, 2, 3, 4, 5, 7])))


class TestNeg(unittest.TestCase):
    def test_negation(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        b = Fp(
            [
                0x669E_44A6_8798_2A79,
                0xA0D9_8A50_37B5_ED71,
                0x0AD5_822F_2861_A854,
                0x96C5_2BF1_EBF7_5781,
                0x87F8_41F0_5C0C_658C,
                0x08A6_E795_AFC5_283E,
            ]
        )
        self.assertTrue((-a).eq(b))

    def test_negation_with_zero(self):
        self.assertTrue(-Fp.zero().is_zero())

    def test_negation_with_max_value(self):
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
        self.assertTrue((-a).eq(b))

    def test_negation_with_small_value(self):
        a = Fp([1, 2, 3, 4, 5, 6])
        b = Fp(
            [
                0xB9FEFFFFFFFFAAAA,
                0x1EABFFFEB153FFFD,
                0x6730D2A0F6B0F621,
                0x64774B84F38512BB,
                0x4B1BA7B6434BACD2,
                0x1A0111EA397FE694,
            ]
        )
        self.assertTrue((-a).eq(b))


class TestAdd(unittest.TestCase):
    def test_addition(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        b = Fp(
            [
                0x9FD2_8773_3D23_DDA0,
                0xB16B_F2AF_738B_3554,
                0x3E57_A75B_D3CC_6D1D,
                0x900B_C0BD_627F_D6D6,
                0xD319_A080_EFB2_45FE,
                0x15FD_CAA4_E4BB_2091,
            ]
        )
        c = Fp(
            [
                0x3934_42CC_B58B_B327,
                0x1092_685F_3BD5_47E3,
                0x3382_252C_AB6A_C4C9,
                0xF946_94CB_7688_7F55,
                0x4B21_5E90_93A5_E071,
                0x0D56_E30F_34F5_F853,
            ]
        )
        self.assertTrue((a + b).eq(c))

    def test_add_zero(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        self.assertTrue((a + Fp.zero()).eq(a))

    def test_add_value_to_its_negation(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        self.assertTrue((a + (-a)).is_zero())

    def test_negative_value_to_another_value(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        b = -Fp(
            [
                0x9FD2_8773_3D23_DDA0,
                0xB16B_F2AF_738B_3554,
                0x3E57_A75B_D3CC_6D1D,
                0x900B_C0BD_627F_D6D6,
                0xD319_A080_EFB2_45FE,
                0x15FD_CAA4_E4BB_2091,
            ]
        )
        c = Fp(
            [
                0x6D8D33E63B434D3D,
                0xEB1282FDB766DD39,
                0x85347BB6F133D6D5,
                0xA21DAA5A9892F727,
                0x3B256CFB3AD8AE23,
                0x155D7199DE7F8464,
            ]
        )
        self.assertTrue((a + b).eq(c))


class TestSub(unittest.TestCase):
    def test_subtraction(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        b = Fp(
            [
                0x9FD2_8773_3D23_DDA0,
                0xB16B_F2AF_738B_3554,
                0x3E57_A75B_D3CC_6D1D,
                0x900B_C0BD_627F_D6D6,
                0xD319_A080_EFB2_45FE,
                0x15FD_CAA4_E4BB_2091,
            ]
        )
        c = Fp(
            [
                0x6D8D_33E6_3B43_4D3D,
                0xEB12_82FD_B766_DD39,
                0x8534_7BB6_F133_D6D5,
                0xA21D_AA5A_9892_F727,
                0x3B25_6CFB_3AD8_AE23,
                0x155D_7199_DE7F_8464,
            ]
        )
        self.assertTrue((a - b).eq(c))

    def test_subtraction_zero(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        self.assertTrue((a - Fp.zero()).eq(a))

    def test_subtract_value_from_itself(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        self.assertTrue((a - a).is_zero())

    def test_subtract_negative_value(self):
        a = Fp(
            [
                0x5360_BB59_7867_8032,
                0x7DD2_75AE_799E_128E,
                0x5C5B_5071_CE4F_4DCF,
                0xCDB2_1F93_078D_BB3E,
                0xC323_65C5_E73F_474A,
                0x115A_2A54_89BA_BE5B,
            ]
        )
        b = -Fp(
            [
                0x9FD2_8773_3D23_DDA0,
                0xB16B_F2AF_738B_3554,
                0x3E57_A75B_D3CC_6D1D,
                0x900B_C0BD_627F_D6D6,
                0xD319_A080_EFB2_45FE,
                0x15FD_CAA4_E4BB_2091,
            ]
        )
        c = Fp(
            [
                0x393442CCB58BB327,
                0x1092685F3BD547E3,
                0x3382252CAB6AC4C9,
                0xF94694CB76887F55,
                0x4B215E9093A5E071,
                0xD56E30F34F5F853,
            ]
        )
        self.assertTrue((a - b).eq(c))


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
        self.assertTrue(Fp.montgomery_reduce(*t_values).eq(expected_result))

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
        self.assertTrue(Fp.montgomery_reduce(*t_values).eq(expected_result))


if __name__ == "__main__":
    unittest.main()
