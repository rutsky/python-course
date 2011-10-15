# -*- encoding: utf-8 -*-

# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import pygame

# Опредилим константы для цветов (модель RGB)
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

# Инициализируем движок pygame
pygame.init()
 
# Инициализируем экран для рисования
size = [700, 500]
screen = pygame.display.set_mode(size)

# Установим заголовок окна
pygame.display.set_caption("My Game")

# Флаг: стоит ли завершить игру
done = False

# Создадим таймер для ограничения числа FPS
clock = pygame.time.Clock()

# ------- главный цикл приложения
while not done:
    # Обработаем события (ввод с клавиатуры, мышь и т.п.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # пользователь нажал кнопку закрытия окна
            done = True # завершить главный цикл на следующей итерации

    # ------- отрисовка
    # Закрасим экран черным цветом
    screen.fill(black)
    # ------- конец отрисовки

    # Ограничиваем частоту обновления экрана 20 кадрами в секунду
    clock.tick(20)

    # Показываем на экран только что нарисованный кадр
    pygame.display.flip()
    
# Корректно завершим работу
pygame.quit()

