from ..genetic import *


class Elitism(Genetic):
    def __init__(self, size: int, elites: int, *args, **kwargs):
        self.population_size = size - elites
        self.elites, self.size = elites, size
        self.name = 'Algorithm: Elitism (%d over %d)' % (elites, size)
        assert size > elites, "Population size less then count of elites"
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        pass

    def join(self, parents: Population, children: Population):
        elites = sorted(parents)[:self.elites]
        mobs = sorted(children)[:self.size - self.elites]
        return elites + mobs


__all__ = [
    'Elitism'
]
