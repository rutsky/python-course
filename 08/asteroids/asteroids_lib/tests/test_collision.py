# -*- encoding: utf-8 -*-

"""Тесты для обработки столкновений"""

import unittest

from asteroids_lib.vector import Vector
from asteroids_lib.collision import closest_vector

class ClosestVectorTest(unittest.TestCase):
    """Тестирование поиска ближайшего вектора в mod n пространстве"""

    def setUp(self):
        # Создаём переменную для хранения размера окна
        self.ss = Vector(10, 10)

        # Создаём тестовые вектора.
        self.v00 = Vector(0, 0)
        self.v50 = Vector(5, 0)
        self.v05 = Vector(0, 5)
        self.v11 = Vector(1, 1)
        self.v99 = Vector(9, 9)

    def test_main(self):
        """Общий тест"""

        self.assertEqual(
            closest_vector(self.ss, self.v00, self.v00),
            self.v00)
        self.assertEqual(
            closest_vector(self.ss, self.v11, self.v99),
            Vector(-2, -2))
        # ...
