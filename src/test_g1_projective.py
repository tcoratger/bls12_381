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
