from ..algorithm import *


class Evolution(Algorithm):
    mu = None
    lmbda = None
    name = 'Algorithm: Evolution'

    def __init__(self,
                 limit: Limit,
                 method,
                 output,
                 mutation,
                 selection
                 ):
        self.mutation = mutation
        self.selection = selection
        super().__init__(limit, method, output)

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
        selected = self.selection.breed(population, self.lmbda)
        children = self.tweak(selected)

        await_list = {}
        for individual in children:
            backdoor = individual.backdoor
            _, estimation = self.method.queue(backdoor)
            if estimation is None:
                await_list[str(backdoor)] = individual
            else:
                individual.set(**estimation)

        while len(await_list) > 0:
            _, estimations = self.method.wait()  # ignore=True)
            for backdoor, estimation in estimations:
                bd_key = str(backdoor)
                individual = await_list.pop(bd_key)
                individual.set(**estimation)

        return self.join(population, children)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
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
    'Limit',
    'Evolution',
    'Population'
]
