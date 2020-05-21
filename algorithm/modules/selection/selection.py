from typing import Iterable
from algorithm.models.individual import Individual, Population


class Selection:
    name = 'Selection'

    def select(self, estimated: Population, size: int) -> Iterable[Individual]:
        raise NotImplementedError

    def configure(self, limits):
        pass

    def __str__(self):
        return self.name


__all__ = [
    'Iterable',
    'Selection',
    'Individual',
    'Population'
]
