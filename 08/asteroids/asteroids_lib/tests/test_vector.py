# -*- encoding: utf-8 -*-

"""Тесты для класса Vector"""

# Для тестирования используем библиотеку Unittest, поставляемую с 
# дистрибутивом Python. Есть и другие библиотеки и даже целые фреймворки 
# для тестирования, предоставляющие более широкие и специфичные возможности.
import unittest

# Тестировать будем класс вектора.
from asteroids_lib.vector import Vector

# Тест --- это код, выполнение которого показывает работает ли какая-то часть
# программы или нет (удовлетворяет ли её работа некоторой спецификации).
# Обычно один тест проверят определённую функцию или класс программы. Чтобы
# проверить всю функциональность программы, пишут множество тестов. Для
# удобства тесты группируют в специальные сущности (терминология зависит от
# фреймворка):
#
#   test       --- проверяет одну функцию/класс на работу с одним определённым
#   входом, test case  --- проверяет одну функцию/класс на набор различных
#   входов, test suite --- набор test case.

# Test case --- это класс, наследующийся от unittest.TestCase
class VectorConstructTestCase(unittest.TestCase):
    """Тесты конструирования класса Vector"""

    # В TestCase все функции, имена которых начинаются на test_*() являются 
    # тестами.
    def test_main(self):
        """Простая проверка конструирования вектора"""

        # Создаём вектор.
        vec = Vector(1, 2)

        # Проверяем, что он создался с переданными значениями x и y, для 
        # этого вызываем Assert ("Утверждение"), предоставляемый 
        # unittest.TestCase.
        self.assertEqual(vec.x, 1) # проверяем, что (vec.x == 1)
        self.assertEqual(vec.y, 2)

        # Если утверждение будет ложным, то библиотека Unittest посчитает, что 
        # тест был провален и сообщит об этом в результатах тестирования.

        # Есть несколько вариаций утверждений:
        # метод                       что проверяет
        # assertEqual(a, b)           a == b   
        # assertNotEqual(a, b)        a != b   
        # assertTrue(x)               bool(x) is True      
        # assertFalse(x)              bool(x) is False     
        # assertIs(a, b)              a is b
        # assertIsNot(a, b)           a is not b
        # assertIsNone(x)             x is None
        # assertIsNotNone(x)          x is not None
        # assertIn(a, b)              a in b
        # assertNotIn(a, b)           a not in b
        # assertIsInstance(a, b)      isinstance(a, b)
        # assertNotIsInstance(a, b)   not isinstance(a, b)

class VectorArithmeticTestCase(unittest.TestCase):
    """Тесты арифметических операций с векторами"""

    # В TestCase можно переопределить два специальных метода setUp() и 
    # tearDown(), которые запускаются соответственно перед выполнением каждого
    # теста и после его завершения, т.о. в них можно делать некоторую общую
    # инициализацию и деинициализацию.
    def setUp(self):
        """Подготавливаем данные для теста"""

        # Создадим несколько векторов на которых будем проводить тестирование.
        self.v00 = Vector(0, 0)
        self.v10 = Vector(1, 0)
        self.v01 = Vector(0, 1)

    def tearDown(self):
        """Уничтожаем ресурсы, выделенные для теста"""

        # Никаких "тяжелых" ресурсов для тестов здесь не выделяется, т.ч. и 
        # освобождать здесь нечего.

    def test_sum(self):
        """Тест сложения"""

        self.assertEqual(self.v00 + self.v00, self.v00) # проверяем, что (v00 + v00 == v00)
        self.assertEqual(self.v00 + self.v10, self.v10)
        self.assertEqual(self.v10 + self.v00, self.v10)
        self.assertEqual(self.v10 + self.v01, Vector(1, 1))

    def test_multiply_by_scalar(self):
        """Тест умножения на число"""

        self.assertEqual(self.v00 * 1, self.v00) # проверяем, что (v00 * 1 == v00)
        self.assertEqual(self.v10 * 30, Vector(30, 0))
        self.assertEqual(self.v01 * 30, Vector(0, 30))
        self.assertEqual(Vector(1, 2) * 30, Vector(30, 60))

if __name__ == '__main__':
    # Вызов unittest.main() просканирует текущий файл на наличие TestCase'ов 
    # (классов, наследующихся от unittest.TestCase). Для каждого из них он 
    # вызовет все тесты (методы классов, кончающиеся на *test()) и проверит,
    # что все тесты успешно завершились и все утверждения (Assert) были 
    # выполнены.
    unittest.main()
