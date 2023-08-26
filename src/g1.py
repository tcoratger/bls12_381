from src.fp import Fp


# This is an element of $\mathbb{G}_1$ represented in the affine coordinate space.
# It is ideal to keep elements in this representation to reduce memory usage and
# improve performance through the use of mixed curve model arithmetic.
# Values of `G1Affine` are guaranteed to be in the $q$-order subgroup unless an
# "unchecked" API was misused.
class G1Affine:
    def __init__(self, x: Fp, y: Fp, inf: bool):
        self.x = x
        self.y = y
        self.infinity = inf

    def identity():
        return G1Affine(Fp.zero(), Fp.one(), True)

    def default():
        return G1Affine.identity()


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
