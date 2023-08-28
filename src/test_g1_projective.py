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
from src.g1 import G1Affine, G1Projective
import random
from src.utils import array_to_number, Choice


class TestG1(unittest.TestCase):
    def test_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.x.is_zero() and a.y.eq(Fp.one()) and a.z.is_zero())

    def test_is_identity(self):
        a = G1Projective.identity()
        self.assertTrue(a.is_identity())


class TestIsOnCurve(unittest.TestCase):
    def test_is_on_curve(self):
        self.assertTrue(G1Projective.identity().is_on_curve())
        self.assertTrue(G1Projective.generator().is_on_curve())

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        gen = G1Affine.generator()
        test = G1Projective(gen.x * z, gen.y * z, z)
        self.assertTrue(test.is_on_curve())
        test.x = z
        self.assertFalse(test.is_on_curve())


class TestEquality(unittest.TestCase):
    def test_projective_point_equality(self):
        a = G1Projective.generator()
        b = G1Projective.identity()

        self.assertTrue(a.eq(a))
        self.assertTrue(b.eq(b))
        self.assertFalse(a.eq(b))
        self.assertFalse(b.eq(a))

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        c = G1Projective(
            a.x * z,
            a.y * z,
            z,
        )

        self.assertTrue(c.is_on_curve())

        self.assertTrue(a.eq(c))
        self.assertFalse(b.eq(c))
        self.assertTrue(c.eq(a))
        self.assertFalse(c.eq(b))

        c.y = -c.y

        self.assertTrue(c.is_on_curve())

        self.assertFalse(a.eq(c))
        self.assertFalse(b.eq(c))
        self.assertFalse(c.eq(a))
        self.assertFalse(c.eq(b))

        c.y = -c.y
        c.x = z

        self.assertFalse(c.is_on_curve())

        self.assertFalse(a.eq(b))
        self.assertFalse(a.eq(c))
        self.assertFalse(b.eq(c))


class TestFromAffine(unittest.TestCase):
    def test_affine_to_projective(self):
        a = G1Affine.generator()
        b = G1Affine.identity()

        self.assertTrue(G1Projective.from_g1_affine(a).is_on_curve())
        self.assertFalse(G1Projective.from_g1_affine(a).is_identity())
        self.assertTrue(G1Projective.from_g1_affine(b).is_on_curve())
        self.assertTrue(G1Projective.from_g1_affine(b).is_identity())


class TestProjectiveAddition(unittest.TestCase):
    def test_projective_addition1(self):
        a = G1Projective.identity()
        b = G1Projective.identity()

        c = a + b

        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

    def test_projective_addition2(self):
        a = G1Projective.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = a + b
        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_projective_addition3(self):
        a = G1Projective.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = b + a

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_projective_addition4(self):
        a = G1Projective.generator().double().double()  # 4P
        b = G1Projective.generator().double()  # 2P

        c = a + b

        d = G1Projective.generator()

        for _ in range(5):
            d += G1Projective.generator()

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

    def test_projective_addition_degenerate(self):
        beta = Fp(
            [
                0xCD03_C9E4_8671_F071,
                0x5DAB_2246_1FCD_A5D2,
                0x5870_42AF_D385_1B95,
                0x8EB6_0EBE_01BA_CB9E,
                0x03F9_7D6E_83D0_50D2,
                0x18F0_2065_5463_8741,
            ]
        )
        beta = beta.square()
        a = G1Projective.generator().double().double()
        b = G1Projective(a.x * beta, -a.y, a.z)

        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())

        c = a + b

        self.assertTrue(
            G1Affine.from_g1_projective(c).eq(
                G1Affine.from_g1_projective(
                    G1Projective(
                        Fp(
                            [
                                0x29E1_E987_EF68_F2D0,
                                0xC5F3_EC53_1DB0_3233,
                                0xACD6_C4B6_CA19_730F,
                                0x18AD_9E82_7BC2_BAB7,
                                0x46E3_B2C5_785C_C7A9,
                                0x07E5_71D4_2D22_DDD6,
                            ]
                        ),
                        Fp(
                            [
                                0x94D1_17A7_E5A5_39E7,
                                0x8E17_EF67_3D4B_5D22,
                                0x9D74_6AAF_508A_33EA,
                                0x8C6D_883D_2516_C9A2,
                                0x0BC3_B8D5_FB04_47F7,
                                0x07BF_A4C7_210F_4F44,
                            ]
                        ),
                        Fp.one(),
                    )
                )
            )
        )

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())


class TestMixedAddition(unittest.TestCase):
    def test_mixed_addition1(self):
        a = G1Affine.identity()
        b = G1Projective.identity()

        c = a + b

        self.assertTrue(c.is_identity())
        self.assertTrue(c.is_on_curve())

    def test_mixed_addition2(self):
        a = G1Affine.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = a + b

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_mixed_addition3(self):
        a = G1Affine.identity()
        b = G1Projective.generator()

        z = Fp(
            [
                0xBA7A_FA1F_9A6F_E250,
                0xFA0F_5B59_5EAF_E731,
                0x3BDC_4776_94C3_06E7,
                0x2149_BE4B_3949_FA24,
                0x64AA_6E06_49B2_078C,
                0x12B1_08AC_3364_3C3E,
            ]
        )

        b.x = b.x * z
        b.y = b.y * z
        b.z = z

        c = b + a

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertTrue(c.eq(G1Projective.generator()))

    def test_mixed_addition4(self):
        a = G1Projective.generator().double().double()  # 4P
        b = G1Projective.generator().double()  # 2P

        c = a + b

        d = G1Projective.generator()

        for _ in range(5):
            d += G1Projective.generator()

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())
        self.assertFalse(d.is_identity())
        self.assertTrue(d.is_on_curve())
        self.assertTrue(c.eq(d))

    def test_projective_addition_degenerate(self):
        beta = Fp(
            [
                0xCD03_C9E4_8671_F071,
                0x5DAB_2246_1FCD_A5D2,
                0x5870_42AF_D385_1B95,
                0x8EB6_0EBE_01BA_CB9E,
                0x03F9_7D6E_83D0_50D2,
                0x18F0_2065_5463_8741,
            ]
        )
        beta = beta.square()
        a = G1Projective.generator().double().double()
        b = G1Projective(a.x * beta, -a.y, a.z)

        a = G1Affine.from_g1_projective(a)

        self.assertTrue(a.is_on_curve())
        self.assertTrue(b.is_on_curve())

        c = a + b

        self.assertTrue(
            G1Affine.from_g1_projective(c).eq(
                G1Affine.from_g1_projective(
                    G1Projective(
                        Fp(
                            [
                                0x29E1_E987_EF68_F2D0,
                                0xC5F3_EC53_1DB0_3233,
                                0xACD6_C4B6_CA19_730F,
                                0x18AD_9E82_7BC2_BAB7,
                                0x46E3_B2C5_785C_C7A9,
                                0x07E5_71D4_2D22_DDD6,
                            ]
                        ),
                        Fp(
                            [
                                0x94D1_17A7_E5A5_39E7,
                                0x8E17_EF67_3D4B_5D22,
                                0x9D74_6AAF_508A_33EA,
                                0x8C6D_883D_2516_C9A2,
                                0x0BC3_B8D5_FB04_47F7,
                                0x07BF_A4C7_210F_4F44,
                            ]
                        ),
                        Fp.one(),
                    )
                )
            )
        )

        self.assertFalse(c.is_identity())
        self.assertTrue(c.is_on_curve())


class TestDoubling(unittest.TestCase):
    def test_doubling1(self):
        tmp = G1Projective.identity().double()

        self.assertTrue(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

    def test_doubling2(self):
        tmp = G1Projective.generator().double()

        self.assertFalse(tmp.is_identity())
        self.assertTrue(tmp.is_on_curve())

        self.assertTrue(
            G1Affine.from_g1_projective(tmp).eq(
                G1Affine(
                    Fp(
                        [
                            0x53E9_78CE_58A9_BA3C,
                            0x3EA0_583C_4F3D_65F9,
                            0x4D20_BB47_F001_2960,
                            0xA54C_664A_E5B2_B5D9,
                            0x26B5_52A3_9D7E_B21F,
                            0x0008_895D_26E6_8785,
                        ]
                    ),
                    Fp(
                        [
                            0x7011_0B32_9829_3940,
                            0xDA33_C539_3F1F_6AFC,
                            0xB86E_DFD1_6A5A_A785,
                            0xAEC6_D1C9_E7B1_C895,
                            0x25CF_C2B5_22D1_1720,
                            0x0636_1C83_F8D0_9B15,
                        ]
                    ),
                    Choice(0),
                )
            )
        )


class TestNegSub(unittest.TestCase):
    def test_affine_negation_and_subtraction(self):
        a = G1Affine.generator()

        self.assertTrue((G1Projective.from_g1_affine(a) + (-a)).is_identity())
        self.assertTrue(
            (G1Projective.from_g1_affine(a) + (-a)).eq(
                G1Projective.from_g1_affine(a) - a
            )
        )
