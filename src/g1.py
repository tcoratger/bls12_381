from src.fp import Fp
from src.utils import (
    sbb,
    mac,
    adc,
    wrapping_mul_u64,
    wrapping_sub_u64,
    CtOption,
    Choice,
)


# This is an element of $\mathbb{G}_1$ represented in the affine coordinate space.
# It is ideal to keep elements in this representation to reduce memory usage and
# improve performance through the use of mixed curve model arithmetic.
# Values of `G1Affine` are guaranteed to be in the $q$-order subgroup unless an
# "unchecked" API was misused.
class G1Affine:
    def __init__(self, x: Fp, y: Fp, inf: Choice):
        self.x = x
        self.y = y
        self.infinity = inf

    def __neg__(self):
        return self.neg()

    def identity():
        return G1Affine(Fp.zero(), Fp.one(), Choice(1))

    def default():
        return G1Affine.identity()

    def conditional_select(a, b, choice: Choice):
        return G1Affine(
            Fp.conditional_select(a.x, b.x, choice),
            Fp.conditional_select(a.y, b.y, choice),
            b.infinity if choice.value else a.infinity,
        )

    # The only cases in which two points are equal are
    # 1. infinity is set on both
    # 2. infinity is not set on both, and their coordinates are equal
    def eq(self, other):
        return (self.infinity and other.infinity) or (
            not self.infinity
            and not other.infinity
            and self.x.eq(other.x)
            and self.y.eq(other.y)
        )

    def from_g1_projective(p):
        zinv = p.z.invert()
        if zinv.choice:
            zinv = zinv.value
        else:
            zinv = Fp.zero()
        x = p.x * zinv
        y = p.y * zinv

        tmp = G1Affine(x, y, Choice(0))

        return G1Affine(
            tmp, G1Affine.identity(), Choice(1) if zinv.is_zero() else Choice(0)
        )


# This is an element of $\mathbb{G}_1$ represented in the projective coordinate space.
class G1Projective:
    def __init__(self, x: Fp, y: Fp, z: Fp):
        self.x = x
        self.y = y
        self.z = z

    def identity():
        return G1Projective(Fp.zero(), Fp.one(), Fp.zero())

    def default():
        return G1Projective.identity()

    def conditional_select(a, b, choice: Choice):
        return G1Projective(
            Fp.conditional_select(a.x, b.x, choice),
            Fp.conditional_select(a.y, b.y, choice),
            Fp.conditional_select(a.z, b.z, choice),
        )
