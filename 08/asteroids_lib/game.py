# -*- encoding: utf-8 -*-

"""Игра Астероиды"""

import pygame
import random
import math
import time

from asteroids_lib.vector import Vector
from asteroids_lib.constants import GlobalConstants, Constants, Color
from asteroids_lib.collision import *
from asteroids_lib.drawing import *
from asteroids_lib.objects import *

class Scene(object):
    """Сцена
    
    Хранит рисуемые и обрабатываемые объекты."""

    def __init__(self, screen_size):
        super(Scene, self).__init__()

        # Списки для астероидов и пуль.
        self.asteroids = []
        self.bullets = []

        # Создаём корабль.
        self.ship = Ship(screen_size / 2.0, Vector(0, 0), Constants.ship_radius)
        self.ship.orientation = math.pi

        # Создаём астероиды.
        for i in xrange(Constants.asteroids_num):
            pos = Vector(random.randint(0, screen_size.x - 1),
                         random.randint(0, screen_size.y - 1))
            max_speed = Constants.asteroid_max_start_speed
            vel = Vector(random.uniform(-max_speed, max_speed),
                         random.uniform(-max_speed, max_speed))
            size = random.random()
            radius = Constants.asteroid_min_start_size + \
                size * (Constants.asteroid_max_start_size - 
                        Constants.asteroid_min_start_size)
            mass = math.pi * radius**2
            self.asteroids.append(Asteroid(pos, vel, radius, mass))

class State(object):
    """Перечисление состояний игры"""

    WAITING_START = 0 # Ожидаем, пока пользователь нажмёт пробел и корабль 
                      # войдёт в игру.
    IN_GAME       = 1 # Корабль в игре.

class Game(object):
    """Игра"""

    def __init__(self, screen_size):
        super(Game, self).__init__()
        self._screen_size = Vector(screen_size[0], screen_size[1])
        self._scene = Scene(self._screen_size)
        self._state = State.WAITING_START

        # Словарь { кнопка: нажата ли }.
        self._keys_state = {}

    def draw(self, screen):
        """Отрисовка сцены"""

        # Отрисуем фон.
        self._draw_background(screen)
        # Отрисуем астероиды.
        self._draw_asteroids(screen)
        # Отрисуем пули.
        self._draw_bullets(screen)

        if self._state == State.WAITING_START:
            # Рисуем корабль не активным, т.к. игра ещё не начата.
            draw_with_duplicates(screen, self._screen_size, 
                self._scene.ship, draw_ship_waiting_start)
        else:
            # Рисуем корабль.
            assert self._state == State.IN_GAME
            draw_with_duplicates(screen, self._screen_size, 
                self._scene.ship, draw_ship_in_game)

    def update(self, dt):
        """Обновляем состояние игры на время dt.
        
        Возвращает:
          True, если игра продолжается, 
          False, если игру необходимо завершить.
        """

        # Список произошедших внешних событий.
        events = list(pygame.event.get())

        # Обработка общих событий для всех состояний игры.
        for event in events:
            if (event.type == pygame.QUIT or
                  (event.type == pygame.KEYDOWN and 
                   event.key == pygame.K_ESCAPE)):
                # Нажат крест на окне или Escape.
                # Прерываем обновление и возвращаем флаг, что необходимо 
                # завершить программу
                return False

            # Обрабатываем события нажатия/отжатия кнопок, чтобы всегда иметь
            # общее состояние клавиатуры.
            if event.type == pygame.KEYDOWN:
                self._keys_state[event.key] = True
            if event.type == pygame.KEYUP:
                self._keys_state[event.key] = False

        # Общая для всех состояний логика: обновить положения астероидов,
        # обновить положения пуль.
        self._move_asteroids(dt)
        self._collide_asteroids()
        self._move_bullets(dt)
        self._update_bullets()
        self._collide_bullets_with_asteroids()
        self._update_ship_orientation(dt)

        # Вызываем функцию обновления, соответствующую состоянию игры.
        if self._state == State.WAITING_START:
            self._update_waiting_start(dt, events)
        else:
            assert self._state == State.IN_GAME
            self._update_in_game(dt, events)

        # Возвращаем флаг, что игру необходимо продолжать
        return True

    def _is_key_down(self, key):
        """Возвращаем состояние кнопки"""
        return self._keys_state.setdefault(key, False)

    def _change_state_to_in_game(self):
        """Функция перехода из состояния AWAITING_START в IN_GAME"""
        self._state = State.IN_GAME

    def _change_state_to_waiting_start(self):
        """Функция перехода из состояния IN_GAME в AWAITING_START"""
        self._state = State.WAITING_START
        self._scene.ship.position = self._screen_size / 2.0
        self._scene.ship.orientation = math.pi
        self._scene.ship.velocity = Vector(0, 0)

    def _update_waiting_start(self, dt, events):
        """Обновление сцены и обработка событий на следующие dt секунд для
        состояния, когда игра ещё не началась
        """
        for event in events:
            if (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_SPACE):
                # Нажат пробел --- переходим в состояние игры.
                self._change_state_to_in_game()
                return

    def _update_in_game(self, dt, events):
        """Обновление сцены и обработка событий на следующие dt секунд для
        состояния, когда игра идёт
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Был нажат пробел --- стреляем.
                    self._scene.bullets.append(
                        self._scene.ship.create_bullet())

        self._update_ship_acceleration(dt)
        self._move_ship(dt)
        self._collide_asteroids_with_ship()

    def _move_ship(self, dt):
        """Обновляем положение корабля"""
        self._scene.ship.update_position(self._screen_size, dt)

    def _update_ship_orientation(self, dt):
        """Обработка нажатия кнопок для поворота корабля"""
        if self._is_key_down(pygame.K_LEFT):
            # Поворачиваем корабль влево.
            self._scene.ship.rotate_left(dt)
        elif self._is_key_down(pygame.K_RIGHT):
            # Поворачиваем корабль вправо.
            self._scene.ship.rotate_right(dt)

    def _update_ship_acceleration(self, dt):
        """Обработка нажатия кнопок для ускорения корабля"""
        if self._is_key_down(pygame.K_UP):
            # Ускориться.
            self._scene.ship.accelerate(dt)
    
    def _move_asteroids(self, dt):
        """Обновляем положения астероидов"""
        for asteroid in self._scene.asteroids:
            asteroid.update_position(self._screen_size, dt)

    def _collide_asteroids(self):
        """Сталкиваем астероиды друг с другом"""
        for i, asteroid1 in enumerate(self._scene.asteroids):
            for asteroid2 in self._scene.asteroids[i + 1:]:
                collide_asteroids(self._screen_size, asteroid1, asteroid2)

    def _move_bullets(self, dt):
        """Обновляем положение пуль"""
        for bullet in self._scene.bullets:
            bullet.update_position(self._screen_size, dt)

    def _update_bullets(self):
        """Удаляем пули, чье время жизни истекло"""

        # Функция filter(func, iter) проходит по всем элементам iter и 
        # записывает в результирующий список лишь те элементы, для которых 
        # func вернёт True.
        self._scene.bullets = filter(
            lambda bullet: not bullet.is_time_exceeded(), self._scene.bullets)

    def _collide_bullets_with_asteroids(self):
        """Сталкиваем пули и астероиды"""
        new_asteroids = []
        for asteroid in self._scene.asteroids:
            for i, bullet in enumerate(self._scene.bullets):
                if is_collides(self._screen_size, asteroid, bullet):
                    new_asteroids.extend(
                        explode_asteroid(self._screen_size, 
                            asteroid, bullet))
                    del self._scene.bullets[i]
                    break
            else:
                new_asteroids.append(asteroid)

        self._scene.asteroids = new_asteroids

    def _collide_asteroids_with_ship(self):
        """Проверяем, не столкнулися ли корабль с астероидом"""
        for asteroid in self._scene.asteroids:
            if is_collides(self._screen_size, asteroid, self._scene.ship):
                self._change_state_to_waiting_start()

    def _draw_background(self, screen):
        """Рисует задний фон"""
        # Заполним фон белым цветом.
        screen.fill(Color.background)

    def _draw_asteroids(self, screen):
        """Рисует все астероиды на сцене"""
        for asteroid in self._scene.asteroids:
            draw_with_duplicates(screen, self._screen_size, 
                asteroid, draw_asteroid)

    def _draw_bullets(self, screen):
        """Рисует все пули на сцене"""
        
        for bullet in self._scene.bullets:
            draw_with_duplicates(screen, self._screen_size, bullet, draw_bullet)

def main_impl():
    # Устанавливаем заголовок окна.
    pygame.display.set_caption('Астероиды')

    # Создаём таймер.
    clock = pygame.time.Clock()

    # Создаём окно для рисования.
    screen = pygame.display.set_mode(GlobalConstants.screen_size)

    # Создаёт объект-игру.
    game = Game(GlobalConstants.screen_size)

    # Инициализируем шаг обновления.
    dt = 1.0 / GlobalConstants.max_fps

    while True:
        # Игра отрисовывает себя.
        game.draw(screen)
        # Результат рисования копируется на физический дисплей.
        pygame.display.flip()

        # Подготовка состояния игры для времени через dt.
        if not game.update(dt):
            # Выходим из игры.
            break

        # Устанавливаем шаг обновления в количество секунд,
        # прошедших с предыдущего вызова clock.tick().
        dt = clock.tick(GlobalConstants.max_fps) / 1000.0

def main():
    # Инициализируем библиотеку PyGame.
    pygame.init()

    try:
        main_impl()
    finally:
        # Всегда деинициализируем библиотеку PyGame, даже в случае падения.
        pygame.quit()
