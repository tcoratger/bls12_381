import unittest
from src.fp import (
    Fp,
)
from src.fp2 import (
    Fp2,
)


class TestFp2(unittest.TestCase):
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
        b = Fp2.from_fp(a)
        self.assertTrue(b.c0.eq(a) and b.c1.eq(Fp.zero()))


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

    def test_equality(self):
        self.assertTrue(
            Fp2(Fp([1, 2, 3, 4, 5, 6]), Fp([7, 8, 9, 10, 11, 12])).eq(
                Fp2(Fp([1, 2, 3, 4, 5, 6]), Fp([7, 8, 9, 10, 11, 12]))
            )
        )

        self.assertFalse(
            Fp2(Fp([2, 2, 3, 4, 5, 6]), Fp([7, 8, 9, 10, 11, 12])).eq(
                Fp2(Fp([1, 2, 3, 4, 5, 6]), Fp([7, 8, 9, 10, 11, 12]))
            )
        )

        self.assertFalse(
            Fp2(Fp([1, 2, 3, 4, 5, 6]), Fp([2, 8, 9, 10, 11, 12])).eq(
                Fp2(Fp([1, 2, 3, 4, 5, 6]), Fp([7, 8, 9, 10, 11, 12]))
            )
        )


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
                    0xF05C_E7CE_9C11_39D7,
                    0x6274_8F57_97E8_A36D,
                    0xC4E8_D9DF_C664_96DF,
                    0xB457_88E1_8118_9209,
                    0x6949_13D0_8772_930D,
                    0x1549_836A_3770_F3CF,
                ]
            ),
            Fp(
                [
                    0x24D0_5BB9_FB9D_491C,
                    0xFB1E_A120_C12E_39D0,
                    0x7067_879F_C807_C7B1,
                    0x60A9_269A_31BB_DAB6,
                    0x45C2_56BC_FD71_649B,
                    0x18F6_9B5D_2B8A_FBDE,
                ]
            ),
        )
        self.assertTrue((-a).eq(b))


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


class TestMul(unittest.TestCase):
    def test_multiplication(self):
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
                    0xF597_483E_27B4_E0F7,
                    0x610F_BADF_811D_AE5F,
                    0x8432_AF91_7714_327A,
                    0x6A9A_9603_CF88_F09E,
                    0xF05A_7BF8_BAD0_EB01,
                    0x0954_9131_C003_FFAE,
                ]
            ),
            Fp(
                [
                    0x963B_02D0_F93D_37CD,
                    0xC95C_E1CD_B30A_73D4,
                    0x3087_25FA_3126_F9B8,
                    0x56DA_3C16_7FAB_0D50,
                    0x6B50_86B5_F4B6_D6AF,
                    0x09C3_9F06_2F18_E9F2,
                ]
            ),
        )
        self.assertTrue((a * b).eq(c))


class TestSquare(unittest.TestCase):
    def test_squaring(self):
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
        self.assertTrue(a.square().eq(b))


class TestFrobenius(unittest.TestCase):
    def test_frobenius_map(self):
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
        self.assertTrue(a.frobenius_map().eq(a.conjugate()))


class TestInvert(unittest.TestCase):
    def test_invert(self):
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
        b = Fp2(
            Fp(
                [
                    0x0581_A133_3D4F_48A6,
                    0x5824_2F6E_F074_8500,
                    0x0292_C955_349E_6DA5,
                    0xBA37_721D_DD95_FCD0,
                    0x70D1_6790_3AA5_DFC5,
                    0x1189_5E11_8B58_A9D5,
                ]
            ),
            Fp(
                [
                    0x0EDA_09D2_D7A8_5D17,
                    0x8808_E137_A7D1_A2CF,
                    0x43AE_2625_C1FF_21DB,
                    0xF85A_C9FD_F7A7_4C64,
                    0x8FCC_DDA5_B8DA_9738,
                    0x08E8_4F0C_B32C_D17D,
                ]
            ),
        )
        self.assertTrue((a.invert().value).eq(b))


class TestSqrt(unittest.TestCase):
    def test_sqrt(self):
        # a = 1488924004771393321054797166853618474668089414631333405711627789629391903630694737978065425271543178763948256226639*u + 784063022264861764559335808165825052288770346101304131934508881646553551234697082295473567906267937225174620141295
        a = Fp2(
            Fp(
                [
                    0x2BEE_D146_27D7_F9E9,
                    0xB661_4E06_660E_5DCE,
                    0x06C4_CC7C_2F91_D42C,
                    0x996D_7847_4B7A_63CC,
                    0xEBAE_BC4C_820D_574E,
                    0x1886_5E12_D93F_D845,
                ]
            ),
            Fp(
                [
                    0x7D82_8664_BAF4_F566,
                    0xD17E_6639_96EC_7339,
                    0x679E_AD55_CB40_78D0,
                    0xFE3B_2260_E001_EC28,
                    0x3059_93D0_43D9_1B68,
                    0x0626_F03C_0489_B72D,
                ]
            ),
        )
        a_sqrt = a.sqrt()
        self.assertTrue((a_sqrt.value.square()).eq(a) and a_sqrt.choice)

        # b = 5, which is a generator of the p - 1 order
        # multiplicative subgroup
        b = Fp2(
            Fp(
                [
                    0x6631_0000_0010_5545,
                    0x2114_0040_0EEC_000D,
                    0x3FA7_AF30_C820_E316,
                    0xC52A_8B8D_6387_695D,
                    0x9FB4_E61D_1E83_EAC5,
                    0x005C_B922_AFE8_4DC7,
                ]
            ),
            Fp.zero(),
        )
        b_sqrt = b.sqrt()
        self.assertTrue((b_sqrt.value.square()).eq(b) and b_sqrt.choice)

        #     c = 25, which is a generator of the (p - 1) / 2 order
        # multiplicative subgroup
        c = Fp2(
            Fp(
                [
                    0x44F6_0000_0051_FFAE,
                    0x86B8_0141_9948_0043,
                    0xD715_9952_F1F3_794A,
                    0x755D_6E3D_FE1F_FC12,
                    0xD36C_D6DB_5547_E905,
                    0x02F8_C8EC_BF18_67BB,
                ]
            ),
            Fp.zero(),
        )
        c_sqrt = c.sqrt()
        self.assertTrue((c_sqrt.value.square()).eq(c) and c_sqrt.choice)

        # 2155129644831861015726826462986972654175647013268275306775721078997042729172900466542651176384766902407257452753362*u + 2796889544896299244102912275102369318775038861758288697415827248356648685135290329705805931514906495247464901062529
        # is nonsquare.
        d = Fp2(
            Fp(
                [
                    0xC5FA_1BC8_FD00_D7F6,
                    0x3830_CA45_4606_003B,
                    0x2B28_7F11_04B1_02DA,
                    0xA7FB_30F2_8230_F23E,
                    0x339C_DB9E_E953_DBF0,
                    0x0D78_EC51_D989_FC57,
                ]
            ),
            Fp(
                [
                    0x27EC_4898_CF87_F613,
                    0x9DE1_394E_1ABB_05A5,
                    0x0947_F85D_C170_FC14,
                    0x586F_BC69_6B61_14B7,
                    0x2B34_75A4_077D_7169,
                    0x13E1_C895_CC4B_6C22,
                ]
            ),
        )
        d_sqrt = d.sqrt()
        self.assertTrue(d_sqrt.value == None and not d_sqrt.choice)

        c.sqrt()


class TestFrobeniusMap(unittest.TestCase):
    def test_frobenius_map(self):
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
                    0xC9A2183163EE70D4,
                    0xBC3770A7196B5C91,
                    0xA247F8C1304C5F44,
                    0xB01FC2A3726C80B5,
                    0xE1D293E5BBD919C9,
                    0x4B78E80020EF2CA,
                ]
            ),
            Fp(
                [
                    0x24D05BB9FB9D491C,
                    0xFB1EA120C12E39D0,
                    0x7067879FC807C7B1,
                    0x60A9269A31BBDAB6,
                    0x45C256BCFD71649B,
                    0x18F69B5D2B8AFBDE,
                ]
            ),
        )
        c = a.frobenius_map()
        self.assertTrue(c.eq(b))
        self.assertTrue(c.c0.eq(a.c0) and c.c1.eq(-(a.c1)))


if __name__ == "__main__":
    unittest.main()
