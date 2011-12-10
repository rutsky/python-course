# -*- encoding: utf-8 -*-

"""Константы"""

import math

class GlobalConstants(object):
    screen_size = (640, 480)
    max_fps = 60

class Constants(object):
    bullet_speed = 250.0
    bullet_range = 300.0
    bullet_radius = 3.0

    ship_radius = 10.0
    # Скорость поворота, радианы/c.
    ship_rotation_speed = math.pi * 2.0
    # Ускорение корабля, пикселы/с^2.
    ship_accel = 50

    asteroids_num = 10
    asteroid_max_start_speed = 30
    asteroid_min_mass = 500.0
    asteroid_min_start_size = 20
    asteroid_max_start_size = 50
    asteroid_mass_division_coef = 3.0
    asteroid_explode_min_coef = 0.5
    asteroid_explode_max_coef = 1.0

class Color(object):
    black    = (   0,   0,   0)
    white    = ( 255, 255, 255)
    blue     = (  50,  50, 255)
    green    = (   0, 255,   0)
    dkgreen  = (   0, 100,   0)
    red      = ( 255,   0,   0)
    purple   = (0xBF,0x0F,0xB5)
    brown    = (0x55,0x33,0x00)
    yellow   = ( 255, 255,   0)

    background = black
    ship_in_game = red
    ship_waiting = green
    bullet = yellow
    asteroid = (127, 127, 127)
