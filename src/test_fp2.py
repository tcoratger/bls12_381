import unittest
from src.fp import (
    Fp,
)
from src.fp2 import (
    Fp2,
)


class TestZero(unittest.TestCase):
    def test_is_zero(self):
        a = Fp2.zero()
        self.assertTrue(a.c0.eq(Fp.zero()) and a.c1.eq(Fp.zero()))


class TestOne(unittest.TestCase):
    def test_one(self):
        a = Fp2.one()
        self.assertTrue(a.c0.eq(Fp.one()) and a.c1.eq(Fp.zero()))


class TestEq(unittest.TestCase):
    def test_eq(self):
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
        c = Fp2(a, b)
        self.assertTrue(c.eq(c))


class TestDefault(unittest.TestCase):
    def test_default(self):
        a = Fp2.default()
        self.assertTrue(a.eq(Fp2.zero()))


class TestIsZero(unittest.TestCase):
    def test_is_zero(self):
        a = Fp2.zero()
        self.assertTrue(a.is_zero())


class TestConjugate(unittest.TestCase):
    def test_conjugate(self):
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
        c = Fp2(a, b)
        d = c.conjugate()
        self.assertTrue(d.c0.eq(c.c0) and d.c1.eq(-(c.c1)))

    def test_conjugate_zero(self):
        a = Fp2(Fp.zero(), Fp.zero())
        b = a.conjugate()
        self.assertTrue(b.eq(Fp2.zero()))


class TestMulByNonResidue(unittest.TestCase):
    def test_mul_by_nonresidue(self):
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
        c = Fp2(a, b)
        d = c.mul_by_nonresidue()
        self.assertTrue(d.c0.eq(a - b) and d.c1.eq(a + b))


class TestLexicographicLargest(unittest.TestCase):
    def test_lexicographic_largest(self):
        self.assertFalse(Fp2.zero().lexicographically_largest())
        self.assertFalse(Fp2.one().lexicographically_largest())
        self.assertTrue(
            Fp2(
                Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp(
                    [
                        0xD328_E37C_C2F5_8D41,
                        0x948D_F085_8A60_5869,
                        0x6032_F9D5_6F93_A573,
                        0x2BE4_83EF_3FFF_DC87,
                        0x30EF_61F8_8F48_3C2A,
                        0x1333_F55A_3572_5BE0,
                    ]
                ),
            ).lexicographically_largest()
        )
        self.assertFalse(
            Fp2(
                -Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                -Fp(
                    [
                        0xD328_E37C_C2F5_8D41,
                        0x948D_F085_8A60_5869,
                        0x6032_F9D5_6F93_A573,
                        0x2BE4_83EF_3FFF_DC87,
                        0x30EF_61F8_8F48_3C2A,
                        0x1333_F55A_3572_5BE0,
                    ]
                ),
            ).lexicographically_largest()
        )
        self.assertFalse(
            Fp2(
                Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp.zero(),
            ).lexicographically_largest()
        )
        self.assertTrue(
            Fp2(
                -Fp(
                    [
                        0x1128_ECAD_6754_9455,
                        0x9E7A_1CFF_3A4E_A1A8,
                        0xEB20_8D51_E08B_CF27,
                        0xE98A_D408_11F5_FC2B,
                        0x736C_3A59_232D_511D,
                        0x10AC_D42D_29CF_CBB6,
                    ]
                ),
                Fp.zero(),
            ).lexicographically_largest()
        )


class TestNeg(unittest.TestCase):
    def test_neg(self):
        a = Fp2(
            Fp(
                [
                    0x1128_ECAD_6754_9455,
                    0x9E7A_1CFF_3A4E_A1A8,
                    0xEB20_8D51_E08B_CF27,
                    0xE98A_D408_11F5_FC2B,
                    0x736C_3A59_232D_511D,
                    0x10AC_D42D_29CF_CBB6,
                ]
            ),
            Fp(
                [
                    0xD328_E37C_C2F5_8D41,
                    0x948D_F085_8A60_5869,
                    0x6032_F9D5_6F93_A573,
                    0x2BE4_83EF_3FFF_DC87,
                    0x30EF_61F8_8F48_3C2A,
                    0x1333_F55A_3572_5BE0,
                ]
            ),
        )
        b = -a
        self.assertTrue(b.c0.eq(-(a.c0)) and b.c1.eq(-(a.c1)))


class TestSub(unittest.TestCase):
    def test_subtraction(self):
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
        b = Fp2(
            Fp(
                [
                    0xA1E0_9175_A4D2_C1FE,
                    0x8B33_ACFC_204E_FF12,
                    0xE244_15A1_1B45_6E42,
                    0x61D9_96B1_B6EE_1936,
                    0x1164_DBE8_667C_853C,
                    0x0788_557A_CC7D_9C79,
                ]
            ),
            Fp(
                [
                    0xDA6A_87CC_6F48_FA36,
                    0x0FC7_B488_277C_1903,
                    0x9445_AC4A_DC44_8187,
                    0x0261_6D5B_C909_9209,
                    0xDBED_4677_2DB5_8D48,
                    0x11B9_4D50_76C7_B7B1,
                ]
            ),
        )
        c = Fp2(
            Fp(
                [
                    0xE1C0_86BB_BF1B_5981,
                    0x4FAF_C3A9_AA70_5D7E,
                    0x2734_B5C1_0BB7_E726,
                    0xB2BD_7776_AF03_7A3E,
                    0x1B89_5FB3_98A8_4164,
                    0x1730_4AEF_6F11_3CEC,
                ]
            ),
            Fp(
                [
                    0x74C3_1C79_9519_1204,
                    0x3271_AA54_79FD_AD2B,
                    0xC9B4_7157_4915_A30F,
                    0x65E4_0313_EC44_B8BE,
                    0x7487_B238_5B70_67CB,
                    0x0952_3B26_D0AD_19A4,
                ]
            ),
        )
        self.assertTrue((a - b).eq(c))


class TestAdd(unittest.TestCase):
    def test_addition(self):
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
        b = Fp2(
            Fp(
                [
                    0xA1E0_9175_A4D2_C1FE,
                    0x8B33_ACFC_204E_FF12,
                    0xE244_15A1_1B45_6E42,
                    0x61D9_96B1_B6EE_1936,
                    0x1164_DBE8_667C_853C,
                    0x0788_557A_CC7D_9C79,
                ]
            ),
            Fp(
                [
                    0xDA6A_87CC_6F48_FA36,
                    0x0FC7_B488_277C_1903,
                    0x9445_AC4A_DC44_8187,
                    0x0261_6D5B_C909_9209,
                    0xDBED_4677_2DB5_8D48,
                    0x11B9_4D50_76C7_B7B1,
                ]
            ),
        )
        c = Fp2(
            Fp(
                [
                    0x6B82_A9A7_08C1_32D2,
                    0x476B_1DA3_39BA_5BA4,
                    0x848C_0E62_4B91_CD87,
                    0x11F9_5955_295A_99EC,
                    0xF337_6FCE_2255_9F06,
                    0x0C3F_E3FA_CE8C_8F43,
                ]
            ),
            Fp(
                [
                    0x6F99_2C12_73AB_5BC5,
                    0x3355_1366_17A1_DF33,
                    0x8B0E_F74C_0AED_AFF9,
                    0x062F_9246_8AD2_CA12,
                    0xE146_9770_738F_D584,
                    0x12C3_C3DD_84BC_A26D,
                ]
            ),
        )
        self.assertTrue((a + b).eq(c))


if __name__ == "__main__":
    unittest.main()
