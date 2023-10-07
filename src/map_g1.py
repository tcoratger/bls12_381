from src.fp import Fp
from src.fp2 import Fp2
from src.fp6 import Fp6
from src.utils import (
    sbb,
    mac,
    adc,
    wrapping_mul_u64,
    wrapping_sub_u64,
    CtOption,
    Choice,
    BLS_X,
    BLS_X_IS_NEGATIVE,
)
from src.scalar import Scalar
from src.fp12 import (
    Fp12,
)
from src.g1 import G1Affine, G1Projective
from src.g2 import G2Affine, G2Projective
from abc import ABC, abstractmethod
from src.chain import chain_pm3div4


# Implementation of hash-to-curve for the G1 group.

# Coefficients of the 11-isogeny x map's numerator
ISO11_XNUM = [
    Fp(
        [
            0x4D18_B6F3_AF00_131C,
            0x19FA_2197_93FE_E28C,
            0x3F28_85F1_467F_19AE,
            0x23DC_EA34_F2FF_B304,
            0xD15B_58D2_FFC0_0054,
            0x0913_BE20_0A20_BEF4,
        ]
    ),
    Fp(
        [
            0x8989_8538_5CDB_BD8B,
            0x3C79_E43C_C7D9_66AA,
            0x1597_E193_F4CD_233A,
            0x8637_EF1E_4D66_23AD,
            0x11B2_2DEE_D20D_827B,
            0x0709_7BC5_9987_84AD,
        ]
    ),
    Fp(
        [
            0xA542_583A_480B_664B,
            0xFC71_69C0_26E5_68C6,
            0x5BA2_EF31_4ED8_B5A6,
            0x5B54_91C0_5102_F0E7,
            0xDF6E_9970_7D2A_0079,
            0x0784_151E_D760_5524,
        ]
    ),
    Fp(
        [
            0x494E_2128_70F7_2741,
            0xAB9B_E52F_BDA4_3021,
            0x26F5_5779_94E3_4C3D,
            0x049D_FEE8_2AEF_BD60,
            0x65DA_DD78_2850_5289,
            0x0E93_D431_EA01_1AEB,
        ]
    ),
    Fp(
        [
            0x90EE_774B_D6A7_4D45,
            0x7ADA_1C8A_41BF_B185,
            0x0F1A_8953_B325_F464,
            0x104C_2421_1BE4_805C,
            0x1691_39D3_19EA_7A8F,
            0x09F2_0EAD_8E53_2BF6,
        ]
    ),
    Fp(
        [
            0x6DDD_93E2_F436_26B7,
            0xA548_2C9A_A1CC_D7BD,
            0x1432_4563_1883_F4BD,
            0x2E0A_94CC_F77E_C0DB,
            0xB028_2D48_0E56_489F,
            0x18F4_BFCB_B436_8929,
        ]
    ),
    Fp(
        [
            0x23C5_F0C9_5340_2DFD,
            0x7A43_FF69_58CE_4FE9,
            0x2C39_0D3D_2DA5_DF63,
            0xD0DF_5C98_E1F9_D70F,
            0xFFD8_9869_A572_B297,
            0x1277_FFC7_2F25_E8FE,
        ]
    ),
    Fp(
        [
            0x79F4_F049_0F06_A8A6,
            0x85F8_94A8_8030_FD81,
            0x12DA_3054_B18B_6410,
            0xE2A5_7F65_0588_0D65,
            0xBBA0_74F2_60E4_00F1,
            0x08B7_6279_F621_D028,
        ]
    ),
    Fp(
        [
            0xE672_45BA_78D5_B00B,
            0x8456_BA9A_1F18_6475,
            0x7888_BFF6_E6B3_3BB4,
            0xE215_85B9_A30F_86CB,
            0x05A6_9CDC_EF55_FEEE,
            0x09E6_99DD_9ADF_A5AC,
        ]
    ),
    Fp(
        [
            0x0DE5_C357_BFF5_7107,
            0x0A0D_B4AE_6B1A_10B2,
            0xE256_BB67_B3B3_CD8D,
            0x8AD4_5657_4E9D_B24F,
            0x0443_915F_50FD_4179,
            0x098C_4BF7_DE8B_6375,
        ]
    ),
    Fp(
        [
            0xE6B0_617E_7DD9_29C7,
            0xFE6E_37D4_4253_7375,
            0x1DAF_DEDA_137A_489E,
            0xE4EF_D1AD_3F76_7CEB,
            0x4A51_D866_7F0F_E1CF,
            0x054F_DF4B_BF1D_821C,
        ]
    ),
    Fp(
        [
            0x72DB_2A50_658D_767B,
            0x8ABF_91FA_A257_B3D5,
            0xE969_D683_3764_AB47,
            0x4641_7014_2A10_09EB,
            0xB14F_01AA_DB30_BE2F,
            0x18AE_6A85_6F40_715D,
        ]
    ),
]

# Coefficients of the 11-isogeny x map's denominator
ISO11_XDEN = [
    Fp(
        [
            0xB962_A077_FDB0_F945,
            0xA6A9_740F_EFDA_13A0,
            0xC14D_568C_3ED6_C544,
            0xB43F_C37B_908B_133E,
            0x9C0B_3AC9_2959_9016,
            0x0165_AA6C_93AD_115F,
        ]
    ),
    Fp(
        [
            0x2327_9A3B_A506_C1D9,
            0x92CF_CA0A_9465_176A,
            0x3B29_4AB1_3755_F0FF,
            0x116D_DA1C_5070_AE93,
            0xED45_3092_4CEC_2045,
            0x0833_83D6_ED81_F1CE,
        ]
    ),
    Fp(
        [
            0x9885_C2A6_449F_ECFC,
            0x4A2B_54CC_D377_33F0,
            0x17DA_9FFD_8738_C142,
            0xA0FB_A727_32B3_FAFD,
            0xFF36_4F36_E54B_6812,
            0x0F29_C13C_6605_23E2,
        ]
    ),
    Fp(
        [
            0xE349_CC11_8278_F041,
            0xD487_228F_2F32_04FB,
            0xC9D3_2584_9ADE_5150,
            0x43A9_2BD6_9C15_C2DF,
            0x1C2C_7844_BC41_7BE4,
            0x1202_5184_F407_440C,
        ]
    ),
    Fp(
        [
            0x587F_65AE_6ACB_057B,
            0x1444_EF32_5140_201F,
            0xFBF9_95E7_1270_DA49,
            0xCCDA_0660_7243_6A42,
            0x7408_904F_0F18_6BB2,
            0x13B9_3C63_EDF6_C015,
        ]
    ),
    Fp(
        [
            0xFB91_8622_CD14_1920,
            0x4A4C_6442_3ECA_DDB4,
            0x0BEB_2329_27F7_FB26,
            0x30F9_4DF6_F83A_3DC2,
            0xAEED_D424_D780_F388,
            0x06CC_402D_D594_BBEB,
        ]
    ),
    Fp(
        [
            0xD41F_7611_51B2_3F8F,
            0x32A9_2465_4357_19B3,
            0x64F4_36E8_88C6_2CB9,
            0xDF70_A9A1_F757_C6E4,
            0x6933_A38D_5B59_4C81,
            0x0C6F_7F72_37B4_6606,
        ]
    ),
    Fp(
        [
            0x693C_0874_7876_C8F7,
            0x22C9_850B_F9CF_80F0,
            0x8E90_71DA_B950_C124,
            0x89BC_62D6_1C7B_AF23,
            0xBC6B_E2D8_DAD5_7C23,
            0x1791_6987_AA14_A122,
        ]
    ),
    Fp(
        [
            0x1BE3_FF43_9C13_16FD,
            0x9965_243A_7571_DFA7,
            0xC7F7_F629_62F5_CD81,
            0x32C6_AA9A_F394_361C,
            0xBBC2_EE18_E1C2_27F4,
            0x0C10_2CBA_C531_BB34,
        ]
    ),
    Fp(
        [
            0x9976_14C9_7BAC_BF07,
            0x61F8_6372_B991_92C0,
            0x5B8C_95FC_1435_3FC3,
            0xCA2B_066C_2A87_492F,
            0x1617_8F5B_BF69_8711,
            0x12A6_DCD7_F0F4_E0E8,
        ]
    ),
    Fp(
        [
            0x7609_0000_0002_FFFD,
            0xEBF4_000B_C40C_0002,
            0x5F48_9857_53C7_58BA,
            0x77CE_5853_7052_5745,
            0x5C07_1A97_A256_EC6D,
            0x15F6_5EC3_FA80_E493,
        ]
    ),
]

# Coefficients of the 11-isogeny y map's numerator
ISO11_YNUM = [
    Fp(
        [
            0x2B56_7FF3_E283_7267,
            0x1D4D_9E57_B958_A767,
            0xCE02_8FEA_04BD_7373,
            0xCC31_A30A_0B6C_D3DF,
            0x7D7B_18A6_8269_2693,
            0x0D30_0744_D42A_0310,
        ]
    ),
    Fp(
        [
            0x99C2_555F_A542_493F,
            0xFE7F_53CC_4874_F878,
            0x5DF0_608B_8F97_608A,
            0x14E0_3832_052B_49C8,
            0x7063_26A6_957D_D5A4,
            0x0A8D_ADD9_C241_4555,
        ]
    ),
    Fp(
        [
            0x13D9_4292_2A5C_F63A,
            0x357E_33E3_6E26_1E7D,
            0xCF05_A27C_8456_088D,
            0x0000_BD1D_E7BA_50F0,
            0x83D0_C753_2F8C_1FDE,
            0x13F7_0BF3_8BBF_2905,
        ]
    ),
    Fp(
        [
            0x5C57_FD95_BFAF_BDBB,
            0x28A3_59A6_5E54_1707,
            0x3983_CEB4_F636_0B6D,
            0xAFE1_9FF6_F97E_6D53,
            0xB346_8F45_5019_2BF7,
            0x0BB6_CDE4_9D8B_A257,
        ]
    ),
    Fp(
        [
            0x590B_62C7_FF8A_513F,
            0x314B_4CE3_72CA_CEFD,
            0x6BEF_32CE_94B8_A800,
            0x6DDF_84A0_9571_3D5F,
            0x64EA_CE4C_B098_2191,
            0x0386_213C_651B_888D,
        ]
    ),
    Fp(
        [
            0xA531_0A31_111B_BCDD,
            0xA14A_C0F5_DA14_8982,
            0xF9AD_9CC9_5423_D2E9,
            0xAA6E_C095_283E_E4A7,
            0xCF5B_1F02_2E1C_9107,
            0x01FD_DF5A_ED88_1793,
        ]
    ),
    Fp(
        [
            0x65A5_72B0_D7A7_D950,
            0xE25C_2D81_8347_3A19,
            0xC2FC_EBE7_CB87_7DBD,
            0x05B2_D36C_769A_89B0,
            0xBA12_961B_E86E_9EFB,
            0x07EB_1B29_C1DF_DE1F,
        ]
    ),
    Fp(
        [
            0x93E0_9572_F7C4_CD24,
            0x364E_9290_7679_5091,
            0x8569_467E_68AF_51B5,
            0xA47D_A894_39F5_340F,
            0xF4FA_9180_82E4_4D64,
            0x0AD5_2BA3_E669_5A79,
        ]
    ),
    Fp(
        [
            0x9114_2984_4E0D_5F54,
            0xD03F_51A3_516B_B233,
            0x3D58_7E56_4053_6E66,
            0xFA86_D2A3_A9A7_3482,
            0xA90E_D5AD_F1ED_5537,
            0x149C_9C32_6A5E_7393,
        ]
    ),
    Fp(
        [
            0x462B_BEB0_3C12_921A,
            0xDC9A_F5FA_0A27_4A17,
            0x9A55_8EBD_E836_EBED,
            0x649E_F8F1_1A4F_AE46,
            0x8100_E165_2B3C_DC62,
            0x1862_BD62_C291_DACB,
        ]
    ),
    Fp(
        [
            0x05C9_B8CA_89F1_2C26,
            0x0194_160F_A9B9_AC4F,
            0x6A64_3D5A_6879_FA2C,
            0x1466_5BDD_8846_E19D,
            0xBB1D_0D53_AF3F_F6BF,
            0x12C7_E1C3_B289_62E5,
        ]
    ),
    Fp(
        [
            0xB55E_BF90_0B8A_3E17,
            0xFEDC_77EC_1A92_01C4,
            0x1F07_DB10_EA1A_4DF4,
            0x0DFB_D15D_C41A_594D,
            0x3895_47F2_334A_5391,
            0x0241_9F98_1658_71A4,
        ]
    ),
    Fp(
        [
            0xB416_AF00_0745_FC20,
            0x8E56_3E9D_1EA6_D0F5,
            0x7C76_3E17_763A_0652,
            0x0145_8EF0_159E_BBEF,
            0x8346_FE42_1F96_BB13,
            0x0D2D_7B82_9CE3_24D2,
        ]
    ),
    Fp(
        [
            0x9309_6BB5_38D6_4615,
            0x6F2A_2619_951D_823A,
            0x8F66_B3EA_5951_4FA4,
            0xF563_E637_04F7_092F,
            0x724B_136C_4CF2_D9FA,
            0x0469_59CF_CFD0_BF49,
        ]
    ),
    Fp(
        [
            0xEA74_8D4B_6E40_5346,
            0x91E9_079C_2C02_D58F,
            0x4106_4965_946D_9B59,
            0xA067_31F1_D2BB_E1EE,
            0x07F8_97E2_67A3_3F1B,
            0x1017_2909_1921_0E5F,
        ]
    ),
    Fp(
        [
            0x872A_A6C1_7D98_5097,
            0xEECC_5316_1264_562A,
            0x07AF_E37A_FFF5_5002,
            0x5475_9078_E5BE_6838,
            0xC4B9_2D15_DB8A_CCA8,
            0x106D_87D1_B51D_13B9,
        ]
    ),
]

# Coefficients of the 11-isogeny y map's denominator
ISO11_YDEN = [
    Fp(
        [
            0xEB6C_359D_47E5_2B1C,
            0x18EF_5F8A_1063_4D60,
            0xDDFA_71A0_889D_5B7E,
            0x723E_71DC_C5FC_1323,
            0x52F4_5700_B70D_5C69,
            0x0A8B_981E_E476_91F1,
        ]
    ),
    Fp(
        [
            0x616A_3C4F_5535_B9FB,
            0x6F5F_0373_95DB_D911,
            0xF25F_4CC5_E35C_65DA,
            0x3E50_DFFE_A3C6_2658,
            0x6A33_DCA5_2356_0776,
            0x0FAD_EFF7_7B6B_FE3E,
        ]
    ),
    Fp(
        [
            0x2BE9_B66D_F470_059C,
            0x24A2_C159_A3D3_6742,
            0x115D_BE7A_D10C_2A37,
            0xB663_4A65_2EE5_884D,
            0x04FE_8BB2_B8D8_1AF4,
            0x01C2_A7A2_56FE_9C41,
        ]
    ),
    Fp(
        [
            0xF27B_F8EF_3B75_A386,
            0x898B_3674_76C9_073F,
            0x2448_2E6B_8C2F_4E5F,
            0xC8E0_BBD6_FE11_0806,
            0x59B0_C17F_7631_448A,
            0x1103_7CD5_8B3D_BFBD,
        ]
    ),
    Fp(
        [
            0x31C7_912E_A267_EEC6,
            0x1DBF_6F1C_5FCD_B700,
            0xD30D_4FE3_BA86_FDB1,
            0x3CAE_528F_BEE9_A2A4,
            0xB1CC_E69B_6AA9_AD9A,
            0x0443_93BB_632D_94FB,
        ]
    ),
    Fp(
        [
            0xC66E_F6EF_EEB5_C7E8,
            0x9824_C289_DD72_BB55,
            0x71B1_A4D2_F119_981D,
            0x104F_C1AA_FB09_19CC,
            0x0E49_DF01_D942_A628,
            0x096C_3A09_7732_72D4,
        ]
    ),
    Fp(
        [
            0x9ABC_11EB_5FAD_EFF4,
            0x32DC_A50A_8857_28F0,
            0xFB1F_A372_1569_734C,
            0xC4B7_6271_EA65_06B3,
            0xD466_A755_99CE_728E,
            0x0C81_D464_5F4C_B6ED,
        ]
    ),
    Fp(
        [
            0x4199_F10E_5B8B_E45B,
            0xDA64_E495_B1E8_7930,
            0xCB35_3EFE_9B33_E4FF,
            0x9E9E_FB24_AA64_24C6,
            0xF08D_3368_0A23_7465,
            0x0D33_7802_3E4C_7406,
        ]
    ),
    Fp(
        [
            0x7EB4_AE92_EC74_D3A5,
            0xC341_B4AA_9FAC_3497,
            0x5BE6_0389_9E90_7687,
            0x03BF_D9CC_A75C_BDEB,
            0x564C_2935_A96B_FA93,
            0x0EF3_C333_71E2_FDB5,
        ]
    ),
    Fp(
        [
            0x7EE9_1FD4_49F6_AC2E,
            0xE5D5_BD5C_B935_7A30,
            0x773A_8CA5_196B_1380,
            0xD0FD_A172_174E_D023,
            0x6CB9_5E0F_A776_AEAD,
            0x0D22_D5A4_0CEC_7CFF,
        ]
    ),
    Fp(
        [
            0xF727_E092_85FD_8519,
            0xDC9D_55A8_3017_897B,
            0x7549_D8BD_0578_94AE,
            0x1784_1961_3D90_D8F8,
            0xFCE9_5EBD_EB5B_490A,
            0x0467_FFAE_F23F_C49E,
        ]
    ),
    Fp(
        [
            0xC176_9E6A_7C38_5F1B,
            0x79BC_930D_EAC0_1C03,
            0x5461_C75A_23ED_E3B5,
            0x6E20_829E_5C23_0C45,
            0x828E_0F1E_772A_53CD,
            0x116A_EFA7_4912_7BFF,
        ]
    ),
    Fp(
        [
            0x101C_10BF_2744_C10A,
            0xBBF1_8D05_3A6A_3154,
            0xA0EC_F39E_F026_F602,
            0xFC00_9D49_96DC_5153,
            0xB900_0209_D5BD_08D3,
            0x189E_5FE4_470C_D73C,
        ]
    ),
    Fp(
        [
            0x7EBD_546C_A157_5ED2,
            0xE47D_5A98_1D08_1B55,
            0x57B2_B625_B6D4_CA21,
            0xB0A1_BA04_2285_20CC,
            0x9873_8983_C210_7FF3,
            0x13DD_DBC4_799D_81D6,
        ]
    ),
    Fp(
        [
            0x0931_9F2E_3983_4935,
            0x039E_952C_BDB0_5C21,
            0x55BA_77A9_A2F7_6493,
            0xFD04_E3DF_C608_6467,
            0xFB95_832E_7D78_742E,
            0x0EF9_C24E_CCAF_5E0E,
        ]
    ),
    Fp(
        [
            0x7609_0000_0002_FFFD,
            0xEBF4_000B_C40C_0002,
            0x5F48_9857_53C7_58BA,
            0x77CE_5853_7052_5745,
            0x5C07_1A97_A256_EC6D,
            0x15F6_5EC3_FA80_E493,
        ]
    ),
]

SSWU_ELLP_A = Fp(
    [
        0x2F65_AA0E_9AF5_AA51,
        0x8646_4C2D_1E84_16C3,
        0xB85C_E591_B7BD_31E2,
        0x27E1_1C91_B5F2_4E7C,
        0x2837_6EDA_6BFC_1835,
        0x1554_55C3_E507_1D85,
    ]
)

SSWU_ELLP_B = Fp(
    [
        0xFB99_6971_FE22_A1E0,
        0x9AA9_3EB3_5B74_2D6F,
        0x8C47_6013_DE99_C5C4,
        0x873E_27C3_A221_E571,
        0xCA72_B5E4_5A52_D888,
        0x0682_4061_418A_386B,
    ]
)

SSWU_XI = Fp(
    [
        0x886C_0000_0023_FFDC,
        0x0F70_008D_3090_001D,
        0x7767_2417_ED58_28C3,
        0x9DAC_23E9_43DC_1740,
        0x5055_3F1B_9C13_1521,
        0x078C_712F_BE0A_B6E8,
    ]
)

SQRT_M_XI_CUBED = Fp(
    [
        0x43B5_71CA_D321_5F1F,
        0xCCB4_60EF_1C70_2DC2,
        0x742D_884F_4F97_100B,
        0xDB2C_3E32_38A3_382B,
        0xE40F_3FA1_3FCE_8F88,
        0x0073_A2AF_9892_A2FF,
    ]
)

# p-1 / 2
P_M1_OVER2 = Fp(
    [
        0xA1FA_FFFF_FFFE_5557,
        0x995B_FFF9_76A3_FFFE,
        0x03F4_1D24_D174_CEB4,
        0xF654_7998_C199_5DBD,
        0x778A_468F_507A_6034,
        0x0205_5993_1F7F_8103,
    ]
)


def from_okm_fp(okm):
    F_2_256 = Fp(
        [
            0x075B_3CD7_C5CE_820F,
            0x3EC6_BA62_1C3E_DB0B,
            0x168A_13D8_2BFF_6BCE,
            0x8766_3C4B_F8C4_49D2,
            0x15F3_4C83_DDC8_D830,
            0x0F96_28B4_9CAA_2E85,
        ]
    )

    bs = bytearray(48)
    bs[16:] = okm[:32]
    db = Fp.from_bytes(bs).value

    bs[16:] = okm[32:]
    da = Fp.from_bytes(bs).value

    return db * F_2_256 + da


def sng0(fp: Fp):
    # Turn into canonical form by computing
    # (a.R) / R = a
    tmp = Fp.montgomery_reduce(
        fp.array[0],
        fp.array[1],
        fp.array[2],
        fp.array[3],
        fp.array[4],
        fp.array[5],
        0,
        0,
        0,
        0,
        0,
        0,
    )

    return Choice(1) if (tmp.array[0] & 1) else Choice(0)


# Maps an element of [`Fp`] to a point on iso-G1.
#
# Implements [section 6.6.2 of `draft-irtf-cfrg-hash-to-curve-12`][sswu].
#
# [sswu]: https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-hash-to-curve-12#section-6.6.2
def map_to_curve_simple_swu(u: Fp):
    usq = u * u
    xi_usq = SSWU_XI * usq
    xisq_u4 = xi_usq.square()
    nd_common = xisq_u4 + xi_usq  # XI^2 * u^4 + XI * u^2

    x_den = SSWU_ELLP_A * Fp.conditional_select(
        -nd_common, SSWU_XI, Choice(1) if nd_common.is_zero() else Choice(0)
    )
    x0_num = SSWU_ELLP_B * (Fp.one() + nd_common)  # B * (1 + (XI^2 * u^4 + XI * u^2))

    # compute g(x0(u))
    x_densq = x_den.square()
    gx_den = x_densq * x_den
    # x0_num^3 + A * x0_num * x_den^2 + B * x_den^3
    gx0_num = (x0_num.square() + SSWU_ELLP_A * x_densq) * x0_num + SSWU_ELLP_B * gx_den

    u_v = gx0_num * gx_den  # u*v
    vsq = gx_den.square()  # v^2
    sqrt_candidate = u_v * chain_pm3div4(u_v * vsq)  # u v (u v^3) ^ ((p - 3) // 4)

    gx0_square = (sqrt_candidate.square() * gx_den).eq(gx0_num)  # g(x0) is square
    x1_num = x0_num * xi_usq
    # sqrt(-XI**3) * u^3 g(x0) ^ ((p - 3) // 4)
    y1 = SQRT_M_XI_CUBED * usq * u * sqrt_candidate

    x_num = Fp.conditional_select(
        x1_num, x0_num, Choice(1) if gx0_square else Choice(0)
    )
    y = Fp.conditional_select(
        y1, sqrt_candidate, Choice(1) if gx0_square else Choice(0)
    )
    y = -y if (sng0(y).value ^ sng0(u).value) == 1 else y

    return G1Projective(x_num, y * x_den, x_den)


# Maps an iso-G1 point to a G1 point.
def iso_map(u: G1Projective):
    COEFFS = [ISO11_XNUM, ISO11_XDEN, ISO11_YNUM, ISO11_YDEN]

    # unpack input point
    x, y, z = u.x, u.y, u.z

    # xnum, xden, ynum, yden
    mapvals = [Fp.zero()] * 4

    # pre-compute powers of z
    zpows = [Fp.zero()] * 15
    zpows[0] = z
    for idx in range(1, len(zpows)):
        zpows[idx] = zpows[idx - 1] * z

    # compute map value by Horner's rule
    for idx in range(4):
        coeff = COEFFS[idx]
        clast = len(coeff) - 1
        mapvals[idx] = coeff[clast]
        for jdx in range(clast):
            mapvals[idx] = mapvals[idx] * x + zpows[jdx] * coeff[clast - 1 - jdx]

    # x denominator is order 1 less than x numerator, so we need an extra factor of z
    mapvals[1] *= z

    # multiply result of Y map by the y-coord, y / z
    mapvals[2] *= y
    mapvals[3] *= z

    return G1Projective(
        x=mapvals[0] * mapvals[3],  # xnum * yden,
        y=mapvals[2] * mapvals[1],  # ynum * xden,
        z=mapvals[1] * mapvals[3],  # xden * yden
    )


def map_to_curve(u: Fp):
    pt = map_to_curve_simple_swu(u)
    return iso_map(pt)


def clear_h(g: G1Projective):
    return g.clear_cofactor()


def check_g1_prime(pt: G1Projective):
    # (X : Y : Z)==(X/Z, Y/Z) is on E': y^2 = x^3 + A * x + B.
    # y^2 z = (x^3) + A (x z^2) + B z^3
    zsq = pt.z.square()
    return (pt.y.square() * pt.z).eq(
        (pt.x.square() * pt.x + SSWU_ELLP_A * pt.x * zsq + SSWU_ELLP_B * zsq * pt.z)
    )
