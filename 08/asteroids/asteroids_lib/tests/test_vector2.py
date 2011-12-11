import math
import unittest

from asteroids_lib.vector import Vector

class SomeVectorTests(unittest.TestCase):
    """Some tests..."""

    def test_rotated(self):
        """Vector rotation test"""

        v10 = Vector(1, 0)
        self.assertTrue(
            (v10.rotated(math.pi / 2.0) - Vector(0, 1)).norm() < 1e-10)
