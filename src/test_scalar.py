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
from src.scalar import Scalar, MODULUS, TWO_INV, ROOT_OF_UNITY, R2, LARGEST
from src.g1 import G1Affine, G1Projective
import random
from src.utils import array_to_number, Choice


class TestBasics(unittest.TestCase):
    def test_from_u64(self):
        a = Scalar.from_u64(10)
        self.assertEqual(a.array, [10, 0, 0, 0])

    def test_eq(self):
        a = Scalar([2, 4, 43, 17])
        self.assertTrue(a.eq(Scalar([2, 4, 43, 17])))

    def test_conditional_select(self):
        a = Scalar([2, 4, 43, 17])
        b = Scalar([45, 2, 4, 10])
        self.assertTrue(Scalar.conditional_select(a, b, Choice(0)).eq(a))
        self.assertTrue(Scalar.conditional_select(a, b, Choice(1)).eq(b))

    def test_zero(self):
        self.assertEqual(Scalar.zero().array, [0, 0, 0, 0])


class TestEquality(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(Scalar.zero().eq(Scalar.zero()))
        self.assertTrue(Scalar.one().eq(Scalar.one()))
        self.assertTrue(R2.eq(R2))
        self.assertFalse(Scalar.one().eq(Scalar.zero()))
        self.assertFalse(Scalar.one().eq(R2))


class TestZero(unittest.TestCase):
    def test_zero(self):
        self.assertTrue(Scalar.zero().eq(-Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() + Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() - Scalar.zero()))
        self.assertTrue(Scalar.zero().eq(Scalar.zero() * Scalar.zero()))


class TestNegation(unittest.TestCase):
    def test_negation(self):
        tmp = -LARGEST
        self.assertTrue(tmp.eq(Scalar([1, 0, 0, 0])))

        tmp = -Scalar.zero()
        self.assertTrue(tmp.eq(Scalar.zero()))

        tmp = -Scalar([1, 0, 0, 0])
        self.assertTrue(tmp.eq(LARGEST))


class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(
            array_to_number(MODULUS.array)
            == 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
        )
        self.assertTrue((Scalar.from_u64(2) * TWO_INV).eq(Scalar.from_u64(1)))
        # self.assertTrue((ROOT_OF_UNITY * ROOT_OF_UNITY).eq(Scalar.from_u64(1)))
