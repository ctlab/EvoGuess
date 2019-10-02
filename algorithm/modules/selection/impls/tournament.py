from ..selection import *
from numpy.random.mtrand import RandomState


class Tournament(Selection):
    def __init__(self, **kwargs):
        self.rounds = kwargs['rounds']
        self.seed = kwargs.get('seed')
        self.rs = RandomState(seed=self.seed)
        self.name = 'Selection: Tournament with %d rounds' % self.rounds

    def select(self, estimated: Population, size: int) -> Iterable[Individual]:
        pass

    def __str__(self):
        return self.name + (' (seed: %s)' % self.seed if self.seed else '')


__all__ = ['Tournament']
