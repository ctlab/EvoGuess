from typing import Tuple
from numpy.random.mtrand import RandomState

from algorithm.models.individual import Individual


class Crossover:
    name = 'Crossover'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed')
        self.rs = RandomState(seed=self.seed)

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        raise NotImplementedError

    def __str__(self):
        return self.name + (' (seed: %s)' % self.seed if self.seed else '')


__all__ = [
    'Tuple',
    'Crossover',
    'Individual'
]
