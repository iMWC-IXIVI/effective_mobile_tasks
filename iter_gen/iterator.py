from exceptions import FibLTZero


class Fib:
    def __init__(self, end):

        if end < 0:
            raise FibLTZero('Введённое число не может быть меньше 0')

        self._end = end
        self._index = 0

    def _fib(self, n: int):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        return self._fib(n - 1) + self._fib(n - 2)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index > self._end:
            raise StopIteration

        self._index += 1
        return self._fib(self._index - 1)
