from ..selection import *
from numpy.random.mtrand import RandomState


class Tournament(Selection):
    def __init__(self, **kwargs):
        self.rounds = kwargs['rounds']
        self.rs = RandomState(seed=kwargs.get('seed'))

    def select(self, estimated: Population, size: int) -> Iterable[Individual]:
        pass

    def __str__(self):
        return 'Selection: tournament with %d rounds' % self.rounds


__all__ = ['Tournament']
