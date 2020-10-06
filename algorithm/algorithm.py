from typing import List, Dict

from .limit.types import *
from algorithm.model import *
from instance.model import Backdoor

from time import time as now

State = Dict[str, int]


class Algorithm:
    name = 'Algorithm'

    def __init__(self,
                 limit: Limit,
                 method,
                 output
                 ):
        self.limit = limit
        self.method = method
        self.output = output

    def initialize(self, backdoor: Backdoor) -> Population:
        raise NotImplementedError

    def iteration(self, population: Population) -> Population:
        raise NotImplementedError

    def start(self, backdoor: Backdoor) -> Population:
        timestamp = now()
        self.limit.set('iteration', 0)
        population = self.initialize(backdoor)
        self.limit.set('time', now() - timestamp)
        self.output.log('Iteration 0', *map(str, population))

        i = 1
        while not self.limit.exhausted():
            self.limit.set('iteration', i)
            population = self.iteration(population)
            self.output.log('\nIteration %d' % i, *map(str, population))
            self.limit.set('time', now() - timestamp)
            i += 1

        return population

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.method,
        ]))


__all__ = [
    'List',
    'Limit',
    'Backdoor',
    'Algorithm',
    'Individual',
    'Population'
]
