import unittest
from src.fp import (
    Fp,
)

from src.utils import array_to_number, Choice

# python3 -m unittest src/test_fp.py


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


class TestSquare(unittest.TestCase):
    def test_squaring(self):
        a = Fp(
            [
                0xD215_D276_8E83_191B,
                0x5085_D80F_8FB2_8261,
                0xCE9A_032D_DF39_3A56,
                0x3E9C_4FFF_2CA0_C4BB,
                0x6436_B6F7_F4D9_5DFB,
                0x1060_6628_AD4A_4D90,
            ]
        )
        b = Fp(
            [
                0x33D9_C42A_3CB3_E235,
                0xDAD1_1A09_4C4C_D455,
                0xA2F1_44BD_729A_AEBA,
                0xD415_0932_BE9F_FEAC,
                0xE27B_C7C4_7D44_EE50,
                0x14B6_A78D_3EC7_A560,
            ]
        )

        self.assertTrue(a.square().eq(b))

    def test_squaring_with_zeros(self):
        self.assertTrue(Fp.zero().square().eq(Fp.zero()))

    def test_squaring_with_ones(self):
        one = Fp([1, 0, 0, 0, 0, 0])
        b = Fp(
            [
                0xF4D38259380B4820,
                0x7FE11274D898FAFB,
                0x343EA97914956DC8,
                0x1797AB1458A88DE9,
                0xED5E64273C4F538B,
                0x14FEC701E8FB0CE9,
            ]
        )
        self.assertTrue(one.square().eq(b))

    def test_squaring_with_negative_numbers(self):
        a = Fp(
            [
                0xD215_D276_8E83_191B,
                0x5085_D80F_8FB2_8261,
                0xCE9A_032D_DF39_3A56,
                0x3E9C_4FFF_2CA0_C4BB,
                0x6436_B6F7_F4D9_5DFB,
                0x1060_6628_AD4A_4D90,
            ]
        )
        self.assertTrue((-a).square().eq(a.square()))

    def test_squaring_with_large_numbers(self):
        large = Fp(
            [
                0xFFFFFFFFFFFFFFFF,
                0xFFFFFFFFFFFFFFFF,
                0xFFFFFFFFFFFFFFFF,
                0xFFFFFFFFFFFFFFFF,
                0xFFFFFFFFFFFFFFFF,
                0xFFFFFFFFFFFFFFFF,
            ]
        )
        expected_large_square = large * large
        self.assertTrue(large.square().eq(expected_large_square))


class TestSqrt(unittest.TestCase):
    def test_sqrt(self):
        a = Fp(
            [
                0xAA27_0000_000C_FFF3,
                0x53CC_0032_FC34_000A,
                0x478F_E97A_6B0A_807F,
                0xB1D3_7EBE_E6BA_24D7,
                0x8EC9_733B_BF78_AB2F,
                0x09D6_4551_3D83_DE7E,
            ]
        )
        b = Fp(
            [
                0x3213_0000_0006_554F,
                0xB93C_0018_D6C4_0005,
                0x5760_5E0D_B0DD_BB51,
                0x8B25_6521_ED1F_9BCB,
                0x6CF2_8D79_0162_2C03,
                0x11EB_AB9D_BB81_E28C,
            ]
        )
        result = a.sqrt()
        self.assertTrue((-(result.value)).eq(b) and result.choice)


class TestInvert(unittest.TestCase):
    def test_inversion(self):
        a = Fp(
            [
                0x43B4_3A50_78AC_2076,
                0x1CE0_7630_46F8_962B,
                0x724A_5276_486D_735C,
                0x6F05_C2A6_282D_48FD,
                0x2095_BD5B_B4CA_9331,
                0x03B3_5B38_94B0_F7DA,
            ]
        )
        b = Fp(
            [
                0x69EC_D704_0952_148F,
                0x985C_CC20_2219_0F55,
                0xE19B_BA36_A9AD_2F41,
                0x19BB_16C9_5219_DBD8,
                0x14DC_ACFD_FB47_8693,
                0x115F_F58A_FFF9_A8E1,
            ]
        )
        result = a.invert()
        self.assertTrue(result.value.eq(b) and result.choice)


class TestFromBytes(unittest.TestCase):
    def test_from_bytes(self):
        result = Fp.from_bytes(
            [
                26,
                1,
                17,
                234,
                57,
                127,
                230,
                154,
                75,
                27,
                167,
                182,
                67,
                75,
                172,
                215,
                100,
                119,
                75,
                132,
                243,
                133,
                18,
                191,
                103,
                48,
                210,
                160,
                246,
                176,
                246,
                36,
                30,
                171,
                255,
                254,
                177,
                83,
                255,
                255,
                185,
                254,
                255,
                255,
                255,
                255,
                170,
                170,
            ]
        )
        self.assertTrue((-Fp.one()).eq(result.value) and result.choice)

    def test_from_bytes_false(self):
        result = Fp.from_bytes(
            [
                27,
                1,
                17,
                234,
                57,
                127,
                230,
                154,
                75,
                27,
                167,
                182,
                67,
                75,
                172,
                215,
                100,
                119,
                75,
                132,
                243,
                133,
                18,
                191,
                103,
                48,
                210,
                160,
                246,
                176,
                246,
                36,
                30,
                171,
                255,
                254,
                177,
                83,
                255,
                255,
                185,
                254,
                255,
                255,
                255,
                255,
                170,
                170,
            ]
        )

        self.assertFalse(result.choice)


class TestSumOfProducts(unittest.TestCase):
    def test_sum_of_products(self):
        a = Fp(
            [
                0x0397_A383_2017_0CD4,
                0x734C_1B2C_9E76_1D30,
                0x5ED2_55AD_9A48_BEB5,
                0x095A_3C6B_22A7_FCFC,
                0x2294_CE75_D4E2_6A27,
                0x1333_8BD8_7001_1EBB,
            ]
        )
        b = Fp(
            [
                0xB9C3_C7C5_B119_6AF7,
                0x2580_E208_6CE3_35C1,
                0xF49A_ED3D_8A57_EF42,
                0x41F2_81E4_9846_E878,
                0xE076_2346_C384_52CE,
                0x0652_E893_26E5_7DC0,
            ]
        )
        c = Fp(
            [
                0xF96E_F3D7_11AB_5355,
                0xE8D4_59EA_00F1_48DD,
                0x53F7_354A_5F00_FA78,
                0x9E34_A4F3_125C_5F83,
                0x3FBE_0C47_CA74_C19E,
                0x01B0_6A8B_BD4A_DFE4,
            ]
        )

        d = Fp(
            [
                0x5D384814D7EF6DF9,
                0x8B5477811C388449,
                0x32DDEA5F318D6A48,
                0x36E9DABCD700040E,
                0xC47BD694ABAB714E,
                0xA838DFE8CBCECD6,
            ]
        )

        self.assertTrue(Fp.sum_of_products([a, b], [a, c]).eq(d))

    def test_sum_of_products_not_same_length(self):
        a = Fp(
            [
                0x0397_A383_2017_0CD4,
                0x734C_1B2C_9E76_1D30,
                0x5ED2_55AD_9A48_BEB5,
                0x095A_3C6B_22A7_FCFC,
                0x2294_CE75_D4E2_6A27,
                0x1333_8BD8_7001_1EBB,
            ]
        )
        b = Fp(
            [
                0xB9C3_C7C5_B119_6AF7,
                0x2580_E208_6CE3_35C1,
                0xF49A_ED3D_8A57_EF42,
                0x41F2_81E4_9846_E878,
                0xE076_2346_C384_52CE,
                0x0652_E893_26E5_7DC0,
            ]
        )

        with self.assertRaises(ValueError) as context:
            Fp.sum_of_products([a, b], [a])

        self.assertEqual(
            str(context.exception),
            "Input lists must have the same length",
        )


class TestLexicographicallyLargest(unittest.TestCase):
    def test_lexicographic_largest_zero(self):
        self.assertFalse(Fp.zero().lexicographically_largest())

    def test_lexicographic_largest_one(self):
        self.assertFalse(Fp.one().lexicographically_largest())

    def test_lexicographic_largest(self):
        self.assertFalse(
            Fp(
                [
                    0xA1FA_FFFF_FFFE_5557,
                    0x995B_FFF9_76A3_FFFE,
                    0x03F4_1D24_D174_CEB4,
                    0xF654_7998_C199_5DBD,
                    0x778A_468F_507A_6034,
                    0x0205_5993_1F7F_8103,
                ]
            ).lexicographically_largest()
        )

        self.assertTrue(
            Fp(
                [
                    0x1804_0000_0001_5554,
                    0x8550_0005_3AB0_0001,
                    0x633C_B57C_253C_276F,
                    0x6E22_D1EC_31EB_B502,
                    0xD391_6126_F2D1_4CA2,
                    0x17FB_B857_1A00_6596,
                ]
            ).lexicographically_largest()
        )

        self.assertTrue(
            Fp(
                [
                    0x43F5_FFFF_FFFC_AAAE,
                    0x32B7_FFF2_ED47_FFFD,
                    0x07E8_3A49_A2E9_9D69,
                    0xECA8_F331_8332_BB7A,
                    0xEF14_8D1E_A0F4_C069,
                    0x040A_B326_3EFF_0206,
                ]
            ).lexicographically_largest()
        )


class TestToBytes(unittest.TestCase):
    def test_to_bytes(self):
        a = Fp(
            [
                0xDC90_6D9B_E3F9_5DC8,
                0x8755_CAF7_4596_91A1,
                0xCFF1_A7F4_E958_3AB3,
                0x9B43_821F_849E_2284,
                0xF575_54F3_A297_4F3F,
                0x085D_BEA8_4ED4_7F79,
            ]
        )
        for _ in range(100):
            a = a.square()
            tmp = a.to_bytes()
            b = Fp.from_bytes(tmp)
            self.assertTrue(a.eq(b.value) and b.choice)


class TestConditionnalSelect(unittest.TestCase):
    def test_conditional_select(self):
        a = Fp(
            [
                0xDC90_6D9B_E3F9_5DC8,
                0x8755_CAF7_4596_91A1,
                0xCFF1_A7F4_E958_3AB3,
                0x9B43_821F_849E_2284,
                0xF575_54F3_A297_4F3F,
                0x085D_BEA8_4ED4_7F79,
            ]
        )
        b = Fp(
            [
                0xA1FA_FFFF_FFFE_5557,
                0x995B_FFF9_76A3_FFFE,
                0x03F4_1D24_D174_CEB4,
                0xF654_7998_C199_5DBD,
                0x778A_468F_507A_6034,
                0x0205_5993_1F7F_8103,
            ]
        )

        self.assertTrue(Fp.conditional_select(a, b, Choice(1)).eq(b))
        self.assertTrue(Fp.conditional_select(a, b, Choice(0)).eq(a))


if __name__ == "__main__":
    unittest.main()
