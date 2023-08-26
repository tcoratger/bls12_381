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
from src.utils import array_to_number, Choice


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


class TestIsZero(unittest.TestCase):
    def test_is_zero(self):
        a = Fp6.zero()
        self.assertTrue(a.is_zero())

        b = Fp6.one()
        self.assertFalse(b.is_zero())


class TestMulByNonresidue(unittest.TestCase):
    def test_mul_by_nonresidue(self):
        a = Fp6.random(random.Random())
        b = a.mul_by_nonresidue()
        self.assertTrue(
            b.c0.eq(a.c2 * Fp2(Fp.one(), Fp.one())) and b.c1.eq(a.c0) and b.c2.eq(a.c1)
        )


class TestArithmetic(unittest.TestCase):
    def test_arithmetic(self):
        a = Fp6(
            Fp2(
                Fp(
                    [
                        0x47F9_CB98_B1B8_2D58,
                        0x5FE9_11EB_A3AA_1D9D,
                        0x96BF_1B5F_4DD8_1DB3,
                        0x8100_D27C_C925_9F5B,
                        0xAFA2_0B96_7464_0EAB,
                        0x09BB_CEA7_D8D9_497D,
                    ]
                ),
                Fp(
                    [
                        0x0303_CB98_B166_2DAA,
                        0xD931_10AA_0A62_1D5A,
                        0xBFA9_820C_5BE4_A468,
                        0x0BA3_643E_CB05_A348,
                        0xDC35_34BB_1F1C_25A6,
                        0x06C3_05BB_19C0_E1C1,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x46F9_CB98_B162_D858,
                        0x0BE9_109C_F7AA_1D57,
                        0xC791_BC55_FECE_41D2,
                        0xF84C_5770_4E38_5EC2,
                        0xCB49_C1D9_C010_E60F,
                        0x0ACD_B8E1_58BF_E3C8,
                    ]
                ),
                Fp(
                    [
                        0x8AEF_CB98_B15F_8306,
                        0x3EA1_108F_E4F2_1D54,
                        0xCF79_F69F_A1B7_DF3B,
                        0xE4F5_4AA1_D16B_1A3C,
                        0xBA5E_4EF8_6105_A679,
                        0x0ED8_6C07_97BE_E5CF,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xCEE5_CB98_B15C_2DB4,
                        0x7159_1082_D23A_1D51,
                        0xD762_30E9_44A1_7CA4,
                        0xD19E_3DD3_549D_D5B6,
                        0xA972_DC17_01FA_66E3,
                        0x12E3_1F2D_D6BD_E7D6,
                    ]
                ),
                Fp(
                    [
                        0xAD2A_CB98_B173_2D9D,
                        0x2CFD_10DD_0696_1D64,
                        0x0739_6B86_C6EF_24E8,
                        0xBD76_E2FD_B1BF_C820,
                        0x6AFE_A7F6_DE94_D0D5,
                        0x1099_4B0C_5744_C040,
                    ]
                ),
            ),
        )

        b = Fp6(
            Fp2(
                Fp(
                    [
                        0xF120_CB98_B16F_D84B,
                        0x5FB5_10CF_F3DE_1D61,
                        0x0F21_A5D0_69D8_C251,
                        0xAA1F_D62F_34F2_839A,
                        0x5A13_3515_7F89_913F,
                        0x14A3_FE32_9643_C247,
                    ]
                ),
                Fp(
                    [
                        0x3516_CB98_B16C_82F9,
                        0x926D_10C2_E126_1D5F,
                        0x1709_E01A_0CC2_5FBA,
                        0x96C8_C960_B825_3F14,
                        0x4927_C234_207E_51A9,
                        0x18AE_B158_D542_C44E,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xBF0D_CB98_B169_82FC,
                        0xA679_10B7_1D1A_1D5C,
                        0xB7C1_47C2_B8FB_06FF,
                        0x1EFA_710D_47D2_E7CE,
                        0xED20_A79C_7E27_653C,
                        0x02B8_5294_DAC1_DFBA,
                    ]
                ),
                Fp(
                    [
                        0x9D52_CB98_B180_82E5,
                        0x621D_1111_5176_1D6F,
                        0xE798_8260_3B48_AF43,
                        0x0AD3_1637_A4F4_DA37,
                        0xAEAC_737C_5AC1_CF2E,
                        0x006E_7E73_5B48_B824,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xE148_CB98_B17D_2D93,
                        0x94D5_1104_3EBE_1D6C,
                        0xEF80_BCA9_DE32_4CAC,
                        0xF77C_0969_2827_95B1,
                        0x9DC1_009A_FBB6_8F97,
                        0x0479_3199_9A47_BA2B,
                    ]
                ),
                Fp(
                    [
                        0x253E_CB98_B179_D841,
                        0xC78D_10F7_2C06_1D6A,
                        0xF768_F6F3_811B_EA15,
                        0xE424_FC9A_AB5A_512B,
                        0x8CD5_8DB9_9CAB_5001,
                        0x0883_E4BF_D946_BC32,
                    ]
                ),
            ),
        )

        c = Fp6(
            Fp2(
                Fp(
                    [
                        0x6934_CB98_B176_82EF,
                        0xFA45_10EA_194E_1D67,
                        0xFF51_313D_2405_877E,
                        0xD0CD_EFCC_2E8D_0CA5,
                        0x7BEA_1AD8_3DA0_106B,
                        0x0C8E_97E6_1845_BE39,
                    ]
                ),
                Fp(
                    [
                        0x4779_CB98_B18D_82D8,
                        0xB5E9_1144_4DAA_1D7A,
                        0x2F28_6BDA_A653_2FC2,
                        0xBCA6_94F6_8BAE_FF0F,
                        0x3D75_E6B8_1A3A_7A5D,
                        0x0A44_C3C4_98CC_96A3,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x8B6F_CB98_B18A_2D86,
                        0xE8A1_1137_3AF2_1D77,
                        0x3710_A624_493C_CD2B,
                        0xA94F_8828_0EE1_BA89,
                        0x2C8A_73D6_BB2F_3AC7,
                        0x0E4F_76EA_D7CB_98AA,
                    ]
                ),
                Fp(
                    [
                        0xCF65_CB98_B186_D834,
                        0x1B59_112A_283A_1D74,
                        0x3EF8_E06D_EC26_6A95,
                        0x95F8_7B59_9214_7603,
                        0x1B9F_00F5_5C23_FB31,
                        0x125A_2A11_16CA_9AB1,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x135B_CB98_B183_82E2,
                        0x4E11_111D_1582_1D72,
                        0x46E1_1AB7_8F10_07FE,
                        0x82A1_6E8B_1547_317D,
                        0x0AB3_8E13_FD18_BB9B,
                        0x1664_DD37_55C9_9CB8,
                    ]
                ),
                Fp(
                    [
                        0xCE65_CB98_B131_8334,
                        0xC759_0FDB_7C3A_1D2E,
                        0x6FCB_8164_9D1C_8EB3,
                        0x0D44_004D_1727_356A,
                        0x3746_B738_A7D0_D296,
                        0x136C_144A_96B1_34FC,
                    ]
                ),
            ),
        )

        self.assertTrue(a.square().eq(a * a))
        self.assertTrue(b.square().eq(b * b))
        self.assertTrue(c.square().eq(c * c))
        self.assertTrue(
            (a.invert().value * b.invert().value).eq((a * b).invert().value)
            and a.invert().choice
            and b.invert().choice
        )
        self.assertTrue(((a + b) * c.square()).eq((c * c * a) + (c * c * b)))
        self.assertTrue((a.invert().value * a).eq(Fp6.one()) and a.invert().choice)

    def test_neg(self):
        a = Fp6.random(random.Random())
        b = -a
        self.assertTrue(b.c0.eq(-(a.c0)) and b.c1.eq(-(a.c1)) and b.c2.eq(-(a.c2)))

    def test_sub(self):
        a = Fp6.random(random.Random())
        b = Fp6.random(random.Random())
        c = a - b
        self.assertTrue(
            c.c0.eq(a.c0 - b.c0) and c.c1.eq(a.c1 - b.c1) and c.c2.eq(a.c2 - b.c2)
        )
        self.assertTrue((a - b + b).eq(a))


class TestFrobeniusMap(unittest.TestCase):
    def test_frobenius_map(self):
        a = Fp6(
            Fp2(
                Fp(
                    [
                        0x47F9_CB98_B1B8_2D58,
                        0x5FE9_11EB_A3AA_1D9D,
                        0x96BF_1B5F_4DD8_1DB3,
                        0x8100_D27C_C925_9F5B,
                        0xAFA2_0B96_7464_0EAB,
                        0x09BB_CEA7_D8D9_497D,
                    ]
                ),
                Fp(
                    [
                        0x0303_CB98_B166_2DAA,
                        0xD931_10AA_0A62_1D5A,
                        0xBFA9_820C_5BE4_A468,
                        0x0BA3_643E_CB05_A348,
                        0xDC35_34BB_1F1C_25A6,
                        0x06C3_05BB_19C0_E1C1,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0x46F9_CB98_B162_D858,
                        0x0BE9_109C_F7AA_1D57,
                        0xC791_BC55_FECE_41D2,
                        0xF84C_5770_4E38_5EC2,
                        0xCB49_C1D9_C010_E60F,
                        0x0ACD_B8E1_58BF_E3C8,
                    ]
                ),
                Fp(
                    [
                        0x8AEF_CB98_B15F_8306,
                        0x3EA1_108F_E4F2_1D54,
                        0xCF79_F69F_A1B7_DF3B,
                        0xE4F5_4AA1_D16B_1A3C,
                        0xBA5E_4EF8_6105_A679,
                        0x0ED8_6C07_97BE_E5CF,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xCEE5_CB98_B15C_2DB4,
                        0x7159_1082_D23A_1D51,
                        0xD762_30E9_44A1_7CA4,
                        0xD19E_3DD3_549D_D5B6,
                        0xA972_DC17_01FA_66E3,
                        0x12E3_1F2D_D6BD_E7D6,
                    ]
                ),
                Fp(
                    [
                        0xAD2A_CB98_B173_2D9D,
                        0x2CFD_10DD_0696_1D64,
                        0x0739_6B86_C6EF_24E8,
                        0xBD76_E2FD_B1BF_C820,
                        0x6AFE_A7F6_DE94_D0D5,
                        0x1099_4B0C_5744_C040,
                    ]
                ),
            ),
        )

        b = Fp6(
            Fp2(
                Fp(
                    [
                        5186400302570941784,
                        6911074806937558429,
                        10862430922382777779,
                        9295661064285167451,
                        12655690643690229419,
                        701381387279223165,
                    ]
                ),
                Fp(
                    [
                        13185189952362216705,
                        5006577082632888997,
                        12071705925372367291,
                        6400713783936774006,
                        7991201011784976177,
                        1386559131812299992,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        11786335780536333254,
                        2738794530956385795,
                        17677701896903356607,
                        14582555561420807680,
                        13249535130151757579,
                        1043730244276007515,
                    ]
                ),
                Fp(
                    [
                        13156777950509169036,
                        7278179170560623574,
                        16614694119003952688,
                        17626640609388795615,
                        8123829316607134470,
                        966903497528890114,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        11922008592636604681,
                        4156845933106861442,
                        8378312071838224846,
                        956966657442801689,
                        6726456622646508829,
                        607724167508366065,
                    ]
                ),
                Fp(
                    [
                        17808920788867655332,
                        5886761442093556132,
                        14062197959221346261,
                        16080155432657655652,
                        15207019238743727378,
                        94959161434845205,
                    ]
                ),
            ),
        )

        aa = Fp6(
            Fp2(
                Fp(
                    [
                        0xF120_CB98_B16F_D84B,
                        0x5FB5_10CF_F3DE_1D61,
                        0x0F21_A5D0_69D8_C251,
                        0xAA1F_D62F_34F2_839A,
                        0x5A13_3515_7F89_913F,
                        0x14A3_FE32_9643_C247,
                    ]
                ),
                Fp(
                    [
                        0x3516_CB98_B16C_82F9,
                        0x926D_10C2_E126_1D5F,
                        0x1709_E01A_0CC2_5FBA,
                        0x96C8_C960_B825_3F14,
                        0x4927_C234_207E_51A9,
                        0x18AE_B158_D542_C44E,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xBF0D_CB98_B169_82FC,
                        0xA679_10B7_1D1A_1D5C,
                        0xB7C1_47C2_B8FB_06FF,
                        0x1EFA_710D_47D2_E7CE,
                        0xED20_A79C_7E27_653C,
                        0x02B8_5294_DAC1_DFBA,
                    ]
                ),
                Fp(
                    [
                        0x9D52_CB98_B180_82E5,
                        0x621D_1111_5176_1D6F,
                        0xE798_8260_3B48_AF43,
                        0x0AD3_1637_A4F4_DA37,
                        0xAEAC_737C_5AC1_CF2E,
                        0x006E_7E73_5B48_B824,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xE148_CB98_B17D_2D93,
                        0x94D5_1104_3EBE_1D6C,
                        0xEF80_BCA9_DE32_4CAC,
                        0xF77C_0969_2827_95B1,
                        0x9DC1_009A_FBB6_8F97,
                        0x0479_3199_9A47_BA2B,
                    ]
                ),
                Fp(
                    [
                        0x253E_CB98_B179_D841,
                        0xC78D_10F7_2C06_1D6A,
                        0xF768_F6F3_811B_EA15,
                        0xE424_FC9A_AB5A_512B,
                        0x8CD5_8DB9_9CAB_5001,
                        0x0883_E4BF_D946_BC32,
                    ]
                ),
            ),
        )

        bb = Fp6(
            Fp2(
                Fp(
                    [
                        17375111219067738187,
                        6896436889723477345,
                        1090334899347964497,
                        12258752208965895066,
                        6490589854421324095,
                        1487311795185238599,
                    ]
                ),
                Fp(
                    [
                        9576962225907902386,
                        10105777654040748704,
                        5775570233413506665,
                        14820926515849450411,
                        140708360471010093,
                        95244719696454220,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        7044013406555139458,
                        11239152779579660354,
                        7047624117909317419,
                        8129917893681583798,
                        17332709215834181339,
                        275462776804833502,
                    ]
                ),
                Fp(
                    [
                        15897662290454840600,
                        16356948449769099132,
                        14488678563205144850,
                        5268066631615219869,
                        16319161763227439869,
                        813250004034655311,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        3460275876402943311,
                        17424264937558314972,
                        6921889031946243686,
                        4472227743734264713,
                        15379038555777104504,
                        674632907673801315,
                    ]
                ),
                Fp(
                    [
                        6415495664835981428,
                        4117334245810148857,
                        17327752396625375173,
                        7204791955339517082,
                        4573297919280158192,
                        831096860460774102,
                    ]
                ),
            ),
        )

        self.assertTrue(a.frobenius_map().eq(b)),
        self.assertTrue(aa.frobenius_map().eq(bb)),


class TestConditionnalSelect(unittest.TestCase):
    def test_conditional_select(self):
        a = Fp6(
            Fp2(
                Fp(
                    [
                        0xF120_CB98_B16F_D84B,
                        0x5FB5_10CF_F3DE_1D61,
                        0x0F21_A5D0_69D8_C251,
                        0xAA1F_D62F_34F2_839A,
                        0x5A13_3515_7F89_913F,
                        0x14A3_FE32_9643_C247,
                    ]
                ),
                Fp(
                    [
                        0x3516_CB98_B16C_82F9,
                        0x926D_10C2_E126_1D5F,
                        0x1709_E01A_0CC2_5FBA,
                        0x96C8_C960_B825_3F14,
                        0x4927_C234_207E_51A9,
                        0x18AE_B158_D542_C44E,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xBF0D_CB98_B169_82FC,
                        0xA679_10B7_1D1A_1D5C,
                        0xB7C1_47C2_B8FB_06FF,
                        0x1EFA_710D_47D2_E7CE,
                        0xED20_A79C_7E27_653C,
                        0x02B8_5294_DAC1_DFBA,
                    ]
                ),
                Fp(
                    [
                        0x9D52_CB98_B180_82E5,
                        0x621D_1111_5176_1D6F,
                        0xE798_8260_3B48_AF43,
                        0x0AD3_1637_A4F4_DA37,
                        0xAEAC_737C_5AC1_CF2E,
                        0x006E_7E73_5B48_B824,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        0xE148_CB98_B17D_2D93,
                        0x94D5_1104_3EBE_1D6C,
                        0xEF80_BCA9_DE32_4CAC,
                        0xF77C_0969_2827_95B1,
                        0x9DC1_009A_FBB6_8F97,
                        0x0479_3199_9A47_BA2B,
                    ]
                ),
                Fp(
                    [
                        0x253E_CB98_B179_D841,
                        0xC78D_10F7_2C06_1D6A,
                        0xF768_F6F3_811B_EA15,
                        0xE424_FC9A_AB5A_512B,
                        0x8CD5_8DB9_9CAB_5001,
                        0x0883_E4BF_D946_BC32,
                    ]
                ),
            ),
        )

        b = Fp6(
            Fp2(
                Fp(
                    [
                        17375111219067738187,
                        6896436889723477345,
                        1090334899347964497,
                        12258752208965895066,
                        6490589854421324095,
                        1487311795185238599,
                    ]
                ),
                Fp(
                    [
                        9576962225907902386,
                        10105777654040748704,
                        5775570233413506665,
                        14820926515849450411,
                        140708360471010093,
                        95244719696454220,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        7044013406555139458,
                        11239152779579660354,
                        7047624117909317419,
                        8129917893681583798,
                        17332709215834181339,
                        275462776804833502,
                    ]
                ),
                Fp(
                    [
                        15897662290454840600,
                        16356948449769099132,
                        14488678563205144850,
                        5268066631615219869,
                        16319161763227439869,
                        813250004034655311,
                    ]
                ),
            ),
            Fp2(
                Fp(
                    [
                        3460275876402943311,
                        17424264937558314972,
                        6921889031946243686,
                        4472227743734264713,
                        15379038555777104504,
                        674632907673801315,
                    ]
                ),
                Fp(
                    [
                        6415495664835981428,
                        4117334245810148857,
                        17327752396625375173,
                        7204791955339517082,
                        4573297919280158192,
                        831096860460774102,
                    ]
                ),
            ),
        )

        self.assertTrue(Fp6.conditional_select(a, b, Choice(1)).eq(b))
        self.assertTrue(Fp6.conditional_select(a, b, Choice(0)).eq(a))


if __name__ == "__main__":
    unittest.main()
