# -*- encoding: utf-8 -*-

"""Объекты игры"""

import time

from asteroids_lib.vector import Vector
from asteroids_lib.constants import Constants

class BaseCircleObject(object):
    """Базовый класс для объектов сцены, аппроксимируемых окружностью"""

    def __init__(self, position, velocity, radius):
        super(BaseCircleObject, self).__init__()
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def round_position(self, screen_size):
        """Переводит позицию в прямоугольник экрана
        
        (При движении объекты могут уходить за край экрана, при этом они
        должны появиться с другой стороны экрана.)
        """
        self.position = \
            (self.position % screen_size + screen_size) % screen_size

    def update_position(self, screen_size, dt):
        """Пересчитывает где будет объект через dt секунд"""
        self.position += self.velocity * dt
        self.round_position(screen_size)

class Asteroid(BaseCircleObject):
    """Астероид"""

    def __init__(self, position, velocity, radius, mass):
        super(Asteroid, self).__init__(position, velocity, radius)
        self.mass = mass

class Ship(BaseCircleObject):
    """Корабль"""

    def __init__(self, position, velocity, radius):
        super(Ship, self).__init__(position, velocity, radius)
        self.orientation = 0

    def create_bullet(self):
        """Создаёт пулю на носу корабля, со скоростью по ориентации корабля"""
        direction = Vector(0, 1).rotated(self.orientation)
        position = self.position + direction * Constants.ship_radius
        time_to_live = Constants.bullet_range / Constants.bullet_speed
        bullet = Bullet(position, 
            self.velocity + direction * Constants.bullet_speed, 
            Constants.bullet_radius, time_to_live)
        return bullet

    def rotate_left(self, dt):
        """Поворот корабля влево"""
        self.orientation -= dt * Constants.ship_rotation_speed

    def rotate_right(self, dt):
        """Поворот корабля вправо"""
        self.orientation += dt * Constants.ship_rotation_speed

    def accelerate(self, dt):
        """Ускорение корабля"""
        direction = Vector(0, 1).rotated(self.orientation)
        self.velocity += dt * Constants.ship_accel * direction

class Bullet(BaseCircleObject):
    """Пуля"""

    def __init__(self, position, velocity, radius, time_to_live):
        super(Bullet, self).__init__(position, velocity, radius)
        self.birth_time = time.time()
        self.time_to_live = time_to_live

    def is_time_exceeded(self):
        """Возвращает истекло ли время жизни пули"""
        return time.time() > self.birth_time + self.time_to_live
