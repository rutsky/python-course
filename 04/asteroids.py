# -*- encoding: utf-8 -*-

"""Игра Астероиды"""

import pygame
import numbers
import random
import math
import time

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

if __name__ == '__main__':
    main()
