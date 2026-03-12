from exceptions import FibLTZero


class Generator:
    def __init__(self, end):

        if end < 0:
            raise FibLTZero('Введённое число не может быть меньше 0')

        self._end = end

    def _fib(self, n: int):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        return self._fib(n - 1) + self._fib(n - 2)

    def __iter__(self):
        for index in range(self._end + 1):
            yield self._fib(index)
