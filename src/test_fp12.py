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
from src.fp12 import (
    Fp12,
)
import random
from src.utils import array_to_number, Choice


class TestFp(unittest.TestCase):
    def test_from_fp(self):
        a = Fp.random(random.Random())
        b = Fp12.from_fp(a)
        self.assertTrue(b.c0.eq(Fp6.from_fp(a)) and b.c1.is_zero())

    def test_from_fp2(self):
        a = Fp2.random(random.Random())
        b = Fp12.from_fp2(a)
        self.assertTrue(b.c0.eq(Fp6.from_fp2(a)) and b.c1.is_zero())

    def test_from_fp6(self):
        a = Fp6.random(random.Random())
        b = Fp12.from_fp6(a)
        self.assertTrue(b.c0.eq(a) and b.c1.is_zero())

    def test_zero(self):
        a = Fp12.zero()
        self.assertTrue(a.c0.is_zero() and a.c1.is_zero())

    def test_is_zero(self):
        a = Fp12.zero()
        self.assertTrue(a.is_zero())

    def test_default(self):
        a = Fp12.default()
        self.assertTrue(a.c0.is_zero() and a.c1.is_zero())

    def test_one(self):
        a = Fp12.one()
        self.assertTrue(a.c0.eq(Fp6.one()) and a.c1.is_zero())


class TestConjugate(unittest.TestCase):
    def test_conjugate(self):
        a = Fp12.random(random.Random())
        b = a.conjugate()
        self.assertTrue(b.c0.eq(a.c0) and b.c1.eq(-a.c1))


class TestArithemetic(unittest.TestCase):
    def test_arithmetic(self):
        a = Fp12(
            Fp6(
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
            ),
            Fp6(
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
            ),
        )

        b = Fp12(
            Fp6(
                Fp2(
                    Fp(
                        [
                            0x47F9_CB98_B1B8_2D58,
                            0x5FE9_11EB_A3AA_1D9D,
                            0x96BF_1B5F_4DD8_1DB3,
                            0x8100_D272_C925_9F5B,
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
                            0x0ACD_B8E1_58BF_E348,
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
            ),
            Fp6(
                Fp2(
                    Fp(
                        [
                            0x47F9_CB98_B1B8_2D58,
                            0x5FE9_11EB_A3AA_1D9D,
                            0x96BF_1B5F_4DD2_1DB3,
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
                            0xCF79_F69F_A117_DF3B,
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
            ),
        )

        c = Fp12(
            Fp6(
                Fp2(
                    Fp(
                        [
                            0x47F9_CB98_71B8_2D58,
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
                            0x7791_BC55_FECE_41D2,
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
                            0xE4F5_4AA1_D16B_133C,
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
                            0xD762_40E9_44A1_7CA4,
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
                            0x1099_4B0C_1744_C040,
                        ]
                    ),
                ),
            ),
            Fp6(
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
                            0xCB49_C1D3_C010_E60F,
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
                            0x1099_4B0C_5744_1040,
                        ]
                    ),
                ),
            ),
        )

        # because a and b and c are similar to each other and
        # I was lazy, this is just some arbitrary way to make
        # them a little more different
        a = (a.square().invert().value).square() + c
        b = (b.square().invert().value).square() + a
        c = (c.square().invert().value).square() + b

        self.assertTrue(a.square().eq(a * a))
        self.assertTrue(b.square().eq(b * b))
        self.assertTrue(c.square().eq(c * c))

        self.assertFalse(a.eq(a.frobenius_map()))
        self.assertTrue(
            a.eq(
                a.frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
                .frobenius_map()
            )
        )

        self.assertTrue(((a + b) * c.square()).eq((c * c * a) + (c * c * b)))
        self.assertTrue(
            (a.invert().value * b.invert().value).eq((a * b).invert().value)
        )
        self.assertTrue((a.invert().value * a).eq(Fp12.one()))


class TestConditionnalSelect(unittest.TestCase):
    def test_conditional_select(self):
        a = Fp12(
            Fp6(
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
            ),
            Fp6(
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
            ),
        )

        b = Fp12(
            Fp6(
                Fp2(
                    Fp(
                        [
                            0x47F9_CB98_B1B8_2D58,
                            0x5FE9_11EB_A3AA_1D9D,
                            0x96BF_1B5F_4DD8_1DB3,
                            0x8100_D272_C925_9F5B,
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
                            0x0ACD_B8E1_58BF_E348,
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
            ),
            Fp6(
                Fp2(
                    Fp(
                        [
                            0x47F9_CB98_B1B8_2D58,
                            0x5FE9_11EB_A3AA_1D9D,
                            0x96BF_1B5F_4DD2_1DB3,
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
                            0xCF79_F69F_A117_DF3B,
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
            ),
        )

        self.assertTrue(Fp12.conditional_select(a, b, Choice(1)).eq(b))
        self.assertTrue(Fp12.conditional_select(a, b, Choice(0)).eq(a))
