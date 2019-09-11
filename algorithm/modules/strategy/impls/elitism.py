import warnings
from math import ceil
from ..strategy import *


class Elitism(Strategy):
    def __init__(self, **kwargs):
        self.elites = kwargs['elites']
        self.popsize = kwargs['popsize']
        self.crossover = kwargs['crossover']
        self.mobs = self.popsize - self.elites
        Strategy.__init__(self, self.popsize, **kwargs)
        if self.mobs % 2 != 0:
            warnings.warn('mob\'s count should be even, but equals %d' % self.mobs, UserWarning)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        j, size = 0, ceil(self.mobs / 2.) * 2
        parents = [next(generator) for _ in range(size)]

        children = []
        while j < len(parents):
            i1, i2 = parents[j], parents[j + 1]
            crossed = self.crossover.cross(i1, i2)
            mutated = map(self.mutation.mutate, crossed)
            children.extend(mutated)
            j += 2

        return parents[:self.elites], children[:self.mobs]

    def __len__(self):
        return self.popsize

    def __str__(self):
        return 'Elitism: %d with %d elites' % (self.popsize, self.elites)


__all__ = ['Elitism']
