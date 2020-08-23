from ..strategy import *

import warnings
from math import ceil
from random import shuffle


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
        # todo: redo
        parents = [next(generator) for _ in range(self.popsize)]
        shuffle(parents)
        children = []
        for i in range(ceil(self.crossed / 2.)):
            i1, i2 = parents[i * 2], parents[i * 2 + 1]
            c1, c2 = self.crossover.cross(i1, i2)
            children.extend([c1, c2])

        children.extend(parents[len(children):])
        # todo: redo
        # children = []
        # for _ in range(ceil(self.crossed / 2.)):
        #     i1, i2 = next(generator), next(generator)
        #     c1, c2 = self.crossover.cross(i1, i2)
        #     children.extend([c1, c2])
        #
        # for _ in range(self.popsize - len(children)):
        #     children.append(next(generator))

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
