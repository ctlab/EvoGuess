from algorithm.map import algorithms

from algorithm.module.mutation import mutations
from algorithm.module.condition import Condition
from algorithm.module.crossover import crossovers
from algorithm.module.strategies import strategies
from algorithm.module.comparator import comparators


class AlgorithmBuilder:
    def __init__(self, name):
        self.name = name
        self.kwargs = {}

    def build(self):
        return algorithms[self.name](**self.kwargs)

    def comparator(self, key, **kwargs):
        self.kwargs['comparator'] = comparators[key](**kwargs)
        return self

    def condition(self, **kwargs):
        self.kwargs['condition'] = Condition(**kwargs)
        return self

    def strategy(self, key, **kwargs):
        self.kwargs['strategy'] = strategies[key](**kwargs)
        return self

    def mutation(self, key, **kwargs):
        self.kwargs['mutation'] = mutations[key](**kwargs)
        return self

    def crossover(self, key, **kwargs):
        self.kwargs['crossover'] = crossovers[key](**kwargs)
        return self
