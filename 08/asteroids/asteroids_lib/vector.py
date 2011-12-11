# -*- encoding: utf-8 -*-

"""Функции и классы для работы с векторами"""

import numbers
import math

class Vector(object):
    """Вектор"""

    def __init__(self, x, y):
        super(Vector, self).__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        """Возвращает строку --- внутреннее представление объекта.
        Нужно, чтобы в интерактивном режиме вектора показывались как 
            Vector(0, 0)
        а не
            <asteroids.Vector instance at 0x2434bd8>
        """
        return "Vector({x},{y})".format(x=self.x, y=self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, vec):
        """Сложение векторов: v1 + v2"""
        assert isinstance(vec, Vector)
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        """Вычитание векторов: v1 - v2"""
        assert isinstance(vec, Vector)
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, scalar):
        """Умножение вектора на число: v * c"""
        assert isinstance(scalar, numbers.Number)
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        """Умножение числа на вектор: c * v"""
        assert isinstance(scalar, numbers.Number)
        return self * scalar

    def __div__(self, scalar):
        """Деление вектора на число: v / c"""
        assert isinstance(scalar, numbers.Number)
        return Vector(self.x / scalar, self.y / scalar)

    def __mod__(self, vec):
        """Покоординатное целочисленное деление: v1 % v2"""
        assert isinstance(vec, Vector)
        return Vector(self.x % vec.x, self.y % vec.y)

    def __and__(self, vec):
        """Скалярное произведение: v1 & v2"""
        assert isinstance(vec, Vector)
        return self.x * vec.x + self.y * vec.y

    def __neg__(self):
        """Унарный минус: -v"""
        return Vector(-self.x, -self.y)

    def rotated(self, angle):
        """Возвращает результат поворота вектора на угол angle (в радианах)
        против часовой стрелки """
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return Vector(x, y)

    def rounded_tuple(self):
        """Округляет координаты и возвращает их в виде кортежа
        
        Для передачи в функции рисования pygame."""
        return (int(self.x), int(self.y))

    def norm(self):
        """Возвращает длину вектора"""
        return (self.x**2 + self.y**2)**0.5

    def normalized(self):
        """Возвращает нормализованный вектор"""
        length = self.norm()
        if length < 1e-10:
            return Vector(0, 0)
        else:
            return self / length
