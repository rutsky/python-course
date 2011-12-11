# -*- encoding: utf-8 -*-

"""Функции обработки столкновений"""

import random
import math

from asteroids_lib.vector import Vector
from asteroids_lib.constants import Constants
from asteroids_lib.objects import Asteroid

def closest_vector(screen_size, pos1, pos2):
    """Возвращает радиус-вектор из первой точки во вторую в mod N
    пространстве"""
    sx, sy = screen_size.x, screen_size.y
    ends = [(pos2 + Vector(sx * dx, sy * dy)) for dy in (-1, 0, 1) 
                                                  for dx in (-1, 0, 1)]

    closest_end = min(ends, key=lambda end: (end - pos1).norm())
    return closest_end - pos1

def distance(screen_size, pos1, pos2):
    """Возвращает расстояние между точками в mod N пространстве"""
    return closest_vector(screen_size, pos1, pos2).norm()

def is_collides(screen_size, obj1, obj2):
    """Проверяет, сталкиваются ли два объекта-окружности"""
    dist = distance(screen_size, obj1.position, obj2.position)
    return dist < obj1.radius + obj2.radius

def collide_asteroids(screen_size, asteroid1, asteroid2):
    """Сталкивает два астероида"""
    if is_collides(screen_size, asteroid1, asteroid2):
        closest_vec = closest_vector(screen_size, 
            asteroid1.position, asteroid2.position)

        # Столкновение.
        vel1_local = asteroid1.velocity - asteroid2.velocity
        if vel1_local.norm() < 1e-10:
            # Астероиды двигаются параллельно.
            return
        if closest_vec.norm() < 1e-10:
            # Астероиды в одной точке, пропустим этот случай (TODO).
            return

        collision_vec = closest_vec.normalized()        
        vel1_x_local = (vel1_local & collision_vec) * collision_vec
        vel1_y_local = vel1_local - vel1_x_local

        mass_sum = asteroid1.mass + asteroid2.mass
        res_vel1_x_local = \
            (asteroid1.mass - asteroid2.mass) / mass_sum * vel1_x_local
        res_vel1_y_local = vel1_y_local
        res_vel1_local = res_vel1_x_local + res_vel1_y_local

        res_vel2_local = \
            2 * asteroid1.mass / mass_sum * vel1_x_local

        res_vel1 = res_vel1_local + asteroid2.velocity
        res_vel2 = res_vel2_local + asteroid2.velocity

        asteroid1.velocity = res_vel1
        asteroid2.velocity = res_vel2

        # Сдвигаем астероиды так, чтобы их окружности больше не пересекались.
        inters_dist = asteroid1.radius + asteroid2.radius - closest_vec.norm()
        asteroid1.position += -collision_vec * (inters_dist + 0.1)
        asteroid1.round_position(screen_size)
        asteroid2.position +=  collision_vec * (inters_dist + 0.1)
        asteroid2.round_position(screen_size)

def explode_asteroid(screen_size, asteroid, bullet):
    """Создаём новые астероиды меньшего размера на месте взорвавшегося 
    старого
    
    Возвращаем список из созданных новых маленьких астероидов.
    """
    if asteroid.mass < Constants.asteroid_min_mass:
        # Слишком маленький астероид --- полностью уничтожаем.
        return []
    else:
        # Делим астероид на два меньших размером.
        mass = asteroid.mass / Constants.asteroid_mass_division_coef
        radius = (mass / math.pi)**0.5

        part1_dir = bullet.velocity.normalized().rotated(+math.pi / 2.0)
        part2_dir = bullet.velocity.normalized().rotated(-math.pi / 2.0)

        vel_factor = random.uniform(
            Constants.asteroid_explode_min_coef,
            Constants.asteroid_explode_max_coef)
        vel1 = asteroid.velocity + part1_dir * asteroid.velocity.norm() * \
            vel_factor
        vel2 = asteroid.velocity + part2_dir * asteroid.velocity.norm() * \
            vel_factor

        pos1 = asteroid.position + part1_dir * radius
        pos2 = asteroid.position + part2_dir * radius

        asteroid1 = Asteroid(pos1, vel1, radius, mass)
        asteroid2 = Asteroid(pos2, vel2, radius, mass)

        return [asteroid1, asteroid2]
