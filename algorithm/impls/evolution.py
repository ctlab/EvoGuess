from ..algorithm import *

from time import time as now


class Evolution(Algorithm):
    name = 'Algorithm: Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strategy = kwargs['strategy']
        self.stagnation_limit = kwargs['stagnation_limit']

    def process(self, backdoor: Backdoor) -> List[Individual]:
        timestamp = now()

        points = []
        self.log_info().log_delim()
        self.limit.set('stagnation', 0)

        root, count = Individual(backdoor), len(self.sampling)
        self.log_it_header(0, 'base').log_delim()
        estimation = self.predict(backdoor, count)
        best = root.set(estimation.value)
        self.log_delim()

        self.limit.set('iteration', 1)
        population = self.strategy.breed([best])
        self.limit.set('time', now() - timestamp)
        while not self.limit.exhausted():
            it = self.limit.get('iteration')
            self.log_it_header(it).log_delim()

            # self.method.switch(population) # todo: integrate

            for individual in population:
                backdoor = individual.backdoor
                estimation = self.predict(backdoor, count)
                if not estimation.from_cache:
                    self.limit.increase('predictions')
                    individual.set(estimation.value)

                    if best > individual:
                        best = individual
                        self.limit.set('stagnation', -1)
                self.log_delim()

            # restart
            self.limit.increase('stagnation')
            if self.limit.get('stagnation') >= self.stagnation_limit:
                points.append(best)
                best = root
                population = self.strategy.breed([root])
                self.limit.set('stagnation', 0)

                # create new log file
                if not self.limit.exhausted():
                    self.output.touch()
                    self.comm.bcast([BTypes.TOUCH.value], root=0)
                    self.log_info().log_delim()
            else:
                population = self.strategy.breed(population)

            self.limit.increase('iteration')
            self.limit.set('time', now() - timestamp)

        if best.value < root.value:
            points.append(best)
            print('Local: %s' % best)

        self.log_delim()
        self.output.log('Points:')
        for point in points:
            self.output.log(str(point))

        return points

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy,
        ]))


__all__ = [
    'Evolution'
]
