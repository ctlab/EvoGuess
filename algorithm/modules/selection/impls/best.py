from ..selection import *


class Best(Selection):
    name = 'Selection: Best'

    def select(self, estimated: Population, size: int) -> Iterable[Individual]:
        estimated.sort()
        i, size = 0, min(size, len(estimated))
        while True:
            yield estimated[i % size]
            i += 1


__all__ = ['Best']
