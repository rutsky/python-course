# -*- coding: utf-8 -*-

class User:
    """Класс пользователя"""
    greeting = "Hello "
    def __init__(self, name):
        self.name = name
    def hello(self):
        return self.greeting + self.name
