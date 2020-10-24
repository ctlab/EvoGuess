from typing import List, Dict

from method import Method
from output import Output
from .limit.types import Limit
from structure.array import Backdoor
from structure.individual import Individual, Population

from time import time as now

State = Dict[str, int]


class Algorithm:
    name = 'Algorithm'

    def __init__(self,
                 limit: Limit,
                 method: Method,
                 output: Output
                 ):
        self.limit = limit
        self.method = method
        self.output = output

    def initialize(self, backdoor: Backdoor) -> Population:
        raise NotImplementedError

    def iteration(self, population: Population) -> Population:
        raise NotImplementedError

    def start(self, backdoor: Backdoor) -> Population:
        self.output.info(self.__str__())

        st_timestamp = now()
        self.limit.set('iteration', 0)
        population = self.initialize(backdoor)
        self.limit.set('time', now() - st_timestamp)
        self._log_iteration(0, population, now() - st_timestamp)

        i = 1
        while not self.limit.exhausted():
            self.limit.set('iteration', i)
            it_timestamp = now()
            population = self.iteration(population)
            self._log_iteration(i, population, now() - it_timestamp)
            self.limit.set('time', now() - st_timestamp)
            i += 1

        return population

    def _log_iteration(self, it, population, time):
        self.output.log(
            'Iteration %d' % it,
            'Individuals (%d):' % len(population),
            *['-- %s' % str(i) for i in population],
            'Time: %.2f' % time,
            '----------------------------------------'
        )

    @staticmethod
    def parse(params):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            '--------------------',
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
