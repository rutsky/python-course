class Reverse(object):
    """Итератор по последовательности в обратном порядке"""
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        # Вернём себя в качестве объекта-итератора
        return self
    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]