# -*- encoding: utf-8 -*-

"""Функции рисования объектов"""

import pygame
import math

from asteroids_lib.vector import Vector
from asteroids_lib.constants import Color
from asteroids_lib.objects import BaseCircleObject

def draw_asteroid(surface, asteroid, position):
    """Рисуем астероид на surface в позиции position"""
    pygame.draw.circle(surface, Color.asteroid, 
        position.rounded_tuple(), 
        int(asteroid.radius) + 1, 0)

def draw_bullet(surface, bullet, position):
    """Рисуем пулю на surface в позиции position"""
    pygame.draw.circle(surface, Color.bullet, 
        position.rounded_tuple(), 
        int(bullet.radius) + 1, 0)

def draw_ship_in_game(surface, ship, position):
    """Рисуем корабль в состоянии IN_GAME на surface в позиции position"""
    top = position + Vector(0, ship.radius).rotated(ship.orientation)
    left = position + \
        Vector(0, ship.radius).rotated(ship.orientation + 5.0 / 6 * math.pi)
    right = position + \
        Vector(0, ship.radius).rotated(ship.orientation - 5.0 / 6 * math.pi)
    pygame.draw.polygon(surface, Color.ship_in_game, 
        [top.rounded_tuple(), left.rounded_tuple(), right.rounded_tuple()], 5)

def draw_ship_waiting_start(surface, ship, position):
    """Рисуем корабль в состоянии WAITING_START на surface в позиции position"""
    top = position + Vector(0, ship.radius).rotated(ship.orientation)
    left = position + \
        Vector(0, ship.radius).rotated(ship.orientation + 5.0 / 6 * math.pi)
    right = position + \
        Vector(0, ship.radius).rotated(ship.orientation - 5.0 / 6 * math.pi)
    pygame.draw.polygon(surface, Color.ship_waiting, 
        [top.rounded_tuple(), left.rounded_tuple(), right.rounded_tuple()], 5)

def draw_with_duplicates(surface, screen_size, obj, draw_func):
    """Вызываем функцию рисования для 9 смещений, чтобы нарисовать все выходы
    за границы экрана"""
    assert isinstance(obj, BaseCircleObject)
    sx, sy = screen_size.x, screen_size.y
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            pos = obj.position + Vector(sx * dx, sy * dy)
            draw_func(surface, obj, pos)
