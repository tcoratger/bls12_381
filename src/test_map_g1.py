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
from src.g1 import G1Affine, G1Projective, BETA
from src.g2 import G2Affine, G2Projective
import random
from src.utils import array_to_number, Choice, BLS_X, BLS_X_IS_NEGATIVE
from src.scalar import Scalar
from src.pairing import (
    MillerLoopResult,
    Gt,
    pairing,
    ell,
    G2Prepared,
    multi_miller_loop,
)

from src.map_g1 import sng0, P_M1_OVER2, map_to_curve_simple_swu, check_g1_prime


class TestSignO(unittest.TestCase):
    def test_sgn0(self):
        self.assertTrue(sng0(Fp.zero()).value == 0)
        self.assertTrue(sng0(Fp.one()).value == 1)
        self.assertTrue(sng0(-Fp.one()).value == 0)
        self.assertTrue(sng0(-Fp.zero()).value == 0)
        self.assertTrue(sng0(P_M1_OVER2).value == 1)
        self.assertTrue(sng0(P_M1_OVER2 + Fp.one()).value == 0)


class TestSimpleSwu(unittest.TestCase):
    def test_simple_swu_expected(self):
        # exceptional case: zero
        p = map_to_curve_simple_swu(Fp.zero())
        x = p.x
        y = p.y
        z = p.z
        xo = Fp(
            [
                0xFB99_6971_FE22_A1E0,
                0x9AA9_3EB3_5B74_2D6F,
                0x8C47_6013_DE99_C5C4,
                0x873E_27C3_A221_E571,
                0xCA72_B5E4_5A52_D888,
                0x0682_4061_418A_386B,
            ]
        )
        yo = Fp(
            [
                0xFD6F_CED8_7A7F_11A3,
                0x9A6B_314B_03C8_DB31,
                0x41F8_5416_E0EA_B593,
                0xFEEB_089F_7E6E_C4D7,
                0x85A1_34C3_7ED1_278F,
                0x0575_C525_BB9F_74BB,
            ]
        )
        zo = Fp(
            [
                0x7F67_4EA0_A891_5178,
                0xB0F9_45FC_13B8_FA65,
                0x4B46_759A_38E8_7D76,
                0x2E7A_9296_41BB_B6A1,
                0x1668_DDFA_462B_F6B6,
                0x0096_0E2E_D1CF_294C,
            ]
        )
        self.assertTrue(x.eq(xo))
        self.assertTrue(y.eq(yo))
        self.assertTrue(z.eq(zo))
        self.assertTrue(check_g1_prime(p))

        # exceptional case: sqrt(-1/XI) (positive)
        excp = Fp(
            [
                0x00F3_D047_7E91_EDBF,
                0x08D6_621E_4CA8_DC69,
                0xB9CF_7927_B19B_9726,
                0xBA13_3C99_6CAF_A2EC,
                0xED2A_5CCD_5CA7_BB68,
                0x19CB_022F_8EE9_D73B,
            ]
        )
        p = map_to_curve_simple_swu(excp)
        x = p.x
        y = p.y
        z = p.z
        self.assertTrue(x.eq(xo))
        self.assertTrue(y.eq(yo))
        self.assertTrue(z.eq(zo))
        self.assertTrue(check_g1_prime(p))

        # exceptional case: sqrt(-1/XI) (negative)
        excp = Fp(
            [
                0xB90B_2FB8_816D_BCEC,
                0x15D5_9DE0_64AB_2396,
                0xAD61_5979_4515_5EFE,
                0xAA64_0EEB_86D5_6FD2,
                0x5DF1_4AE8_E6A3_F16E,
                0x0036_0FBA_AA96_0F5E,
            ]
        )
        p = map_to_curve_simple_swu(excp)
        x = p.x
        y = p.y
        z = p.z
        myo = -yo
        self.assertTrue(x.eq(xo))
        self.assertTrue(y.eq(myo))
        self.assertTrue(z.eq(zo))
        self.assertTrue(check_g1_prime(p))

        u = Fp(
            [
                0xA618_FA19_F7E2_EADC,
                0x93C7_F1FC_876B_A245,
                0xE2ED_4CC4_7B5C_0AE0,
                0xD49E_FA74_E4A8_D000,
                0xA0B2_3BA6_92B5_431C,
                0x0D15_51F2_D7D8_D193,
            ]
        )
        xo = Fp(
            [
                0x2197_CA55_FAB3_BA48,
                0x591D_EB39_F434_949A,
                0xF9DF_7FB4_F1FA_6A08,
                0x59E3_C16A_9DFA_8FA5,
                0xE592_9B19_4AAD_5F7A,
                0x130A_46A4_C61B_44ED,
            ]
        )
        yo = Fp(
            [
                0xF721_5B58_C720_0AD0,
                0x8905_1631_3A4E_66BF,
                0xC903_1ACC_8A36_19A8,
                0xEA1F_9978_FDE3_FFEC,
                0x0548_F02D_6CFB_F472,
                0x1693_7557_3529_163F,
            ]
        )
        zo = Fp(
            [
                0xF36F_EB2E_1128_ADE0,
                0x42E2_2214_250B_CD94,
                0xB94F_6BA2_DDDF_62D6,
                0xF56D_4392_782B_F0A2,
                0xB2D7_CE1E_C263_09E7,
                0x182B_57ED_6B99_F0A1,
            ]
        )
        p = map_to_curve_simple_swu(u)
        x = p.x
        y = p.y
        z = p.z
        self.assertTrue(x.eq(xo))
        self.assertTrue(y.eq(yo))
        self.assertTrue(z.eq(zo))
        self.assertTrue(check_g1_prime(p))
