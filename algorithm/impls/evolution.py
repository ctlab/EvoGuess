from ..algorithm import *

from time import time as now


class Evolution(Algorithm):
    name = 'Algorithm: Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strategy = kwargs['strategy']
        self.stagnation_limit = kwargs['stagnation_limit']

    def process(self, backdoor: Backdoor) -> List[Individual]:
        points = []
        timestamp = now()

        self.log_info().log_delim()
        self.limit.set('stagnation', 0)

        root = Individual(backdoor)
        count = self.sampling.get_size(backdoor)
        self.log_it_header(0, 'base').log_delim()
        estimation = self.predict(backdoor, count)
        best = root.set(estimation.value)
        self.log_delim()

        self.limit.set('iteration', 1)
        population = [best]
        offspring = self.strategy.breed(population)
        self.limit.set('time', now() - timestamp)
        while not self.limit.exhausted():
            it = self.limit.get('iteration')
            self.log_it_header(it).log_delim()

            # self.method.switch(population) # todo: integrate

            for individual in offspring:
                backdoor = individual.backdoor
                count = self.sampling.get_size(backdoor)
                estimation = self.predict(backdoor, count)
                if not estimation.from_cache:
                    self.limit.increase('predictions')
                    individual.set(estimation.value)

                    if best > individual:
                        best = individual
                        self.limit.set('stagnation', -1)
                self.log_delim()

            pop = self.strategy.selection.select(population + offspring, len(offspring))
            population = [next(pop) for _ in range(len(offspring))]

            # restart
            self.limit.increase('iteration')
            self.limit.increase('stagnation')
            if self.limit.get('stagnation') >= self.stagnation_limit:
                points.append(best)
                best = root
                self.limit.set('stagnation', 0)
                info = self.strategy.configure(self.limit.limits)
                self.output.debug(3, 1, 'configure: ' + str(info))
                population = [root]
                offspring = self.strategy.breed(population)

                # create new log file
                if not self.limit.exhausted():
                    self.touch_log().log_info().log_delim()
            else:
                info = self.strategy.configure(self.limit.limits)
                self.output.debug(3, 1, 'configure: ' + str(info))
                offspring = self.strategy.breed(population)

            self.limit.set('time', now() - timestamp)

        if best.value < root.value:
            points.append(best)

        return points

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy,
            'Stagnations: %d' % self.stagnation_limit,
        ]))


__all__ = [
    'Evolution'
]
