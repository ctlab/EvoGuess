from ..algorithm import *

from .mutation.mutation import Mutation
from .selection.selection import Selection


class Evolution(Algorithm):
    population_size = None
    name = 'Algorithm: Evolution'

    def __init__(self,
                 mutation: Mutation,
                 selection: Selection,
                 *args, **kwargs
                 ):
        self.mutation = mutation
        self.selection = selection
        super().__init__(*args, **kwargs)

    def initialize(self, backdoor: Backdoor) -> Population:
        root = Individual(backdoor)
        _, estimation = self.method.queue(backdoor)
        if estimation is None:
            _, estimations = self.method.wait()  # ignore=True)
            estimation = list(estimations)[0]
            assert backdoor == estimation[0]
            estimation = estimation[1]

        best = root.set(**estimation)
        return [best]

    def iteration(self, population: Population) -> Population:
        selected = self.selection.breed(population, self.population_size)
        children = self.tweak(selected)

        await_list = {}
        for individual in children:
            backdoor = individual.backdoor
            job_id, estimation = self.method.queue(backdoor)
            if estimation is None:
                bd_key = str(backdoor)
                if bd_key not in await_list:
                    await_list[bd_key] = []
                await_list[bd_key].append(individual)
            else:
                individual.set(**estimation)

        while len(await_list) > 0:
            _, estimations = self.method.wait()  # ignore=True)
            for backdoor, estimation in estimations:
                bd_key = str(backdoor)
                individuals = await_list.pop(bd_key)
                for individual in individuals:
                    individual.set(**estimation)

        return self.join(population, children)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    @staticmethod
    def parse(params):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.selection,
            self.mutation,
            '--------------------',
            self.method,
        ]))


__all__ = [
    'Evolution',
    'Population'
]
