from ..selection import *
from numpy.random.mtrand import RandomState


class Roulette(Selection):
    name = 'Selection: Roulette'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed')
        self.rs = RandomState(seed=self.seed)

    def select(self, estimated: Population, size: int) -> Iterable[Individual]:
        ranges, rng, count = [], 0, len(estimated)

        for i in range(count):
            w = 0.
            for j in range(count):
                w += estimated[i].value / estimated[j].value
            rng = rng + (1. / w) if (i != count - 1) else 1.
            ranges.append(rng)

        def get(p):
            for k in range(count):
                if ranges[k] >= p:
                    return estimated[k]

        while True:
            yield get(self.rs.rand())

    def __str__(self):
        return self.name + (' (seed: %s)' % self.seed if self.seed else '')


__all__ = ['Roulette']
