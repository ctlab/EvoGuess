from ..strategy import *

import warnings
from math import ceil


class Genetic(Strategy):
    def __init__(self, **kwargs):
        self.crossed = kwargs['mu']
        self.popsize = kwargs['lmbda']
        self.crossover = kwargs['crossover']
        super().__init__(self.popsize, **kwargs)
        self.name = 'Strategy: Genetic (%d of %d)' % (self.crossed, self.popsize)
        if self.crossed % 2 != 0:
            warnings.warn('count of crossed children should be even, but equals %d' % self.crossed, UserWarning)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        children = []
        for _ in range(ceil(self.crossed / 2.)):
            i1, i2 = next(generator), next(generator)
            c1, c2 = self.crossover.cross(i1, i2)
            children.extend([c1, c2])

        for _ in range(self.popsize - len(children)):
            children.append(next(generator))

        return [], list(map(self.mutation.mutate, children))

    def configure(self, limits):
        return [
            *super().configure(limits),
            self.crossover.configure(limits)
        ]

    def __len__(self):
        return self.popsize

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.crossover
        ]))


__all__ = ['Genetic']
