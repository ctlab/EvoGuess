from typing import Sequence

from ..algorithm import *

from time import time as now
from deap import tools, creator, base


class MultiEvolution(Algorithm):
    name = 'Algorithm: Multi Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weights = kwargs['weights']
        self.strategy = kwargs['strategy']
        self.stagnation_limit = kwargs['stagnation_limit']

    def process(self, backdoor: Backdoor) -> List[Individual]:
        self.output.st_timer(self.name, 'algorithm')
        timestamp = now()
        front, points = tools.ParetoFront(), []

        creator.create("Fitness", base.Fitness, weights=self.weights)
        creator.create("Individual", Individual, fitness=creator.Fitness)

        self.log_info().log_delim()
        self.limit.set('stagnation', 0)

        self.output.st_timer('Evolution_init', 'init')
        root = creator.Individual(backdoor)
        count = self.sampling.get_size(backdoor)
        self.log_it_header(0, 'base').log_delim()
        estimation = self.predict(backdoor, count)
        best = root.set(estimation.value)
        root.fitness.values = (estimation.value, estimation.value_sd())
        self.log_delim()
        self.output.ed_timer('Evolution_init')

        population = [root]
        pop = self.strategy.breed(population)
        offspring = [creator.Individual(ind.backdoor) for ind in pop]

        self.limit.set('iteration', 1)
        self.limit.set('time', now() - timestamp)
        while not self.limit.exhausted():
            it = self.limit.get('iteration')
            self.log_it_header(it).log_delim()
            self.output.st_timer('Evolution_iteration_%d' % it, 'iteration')

            self.output.st_timer('Evolution_evaluate', 'evaluate')
            for individual in offspring:
                backdoor = individual.backdoor
                count = self.sampling.get_size(backdoor)
                estimation = self.predict(backdoor, count)
                if not estimation.from_cache:
                    self.limit.increase('predictions')

                individual.set(estimation.value)
                individual.fitness.values = (estimation.value, estimation.value_sd())
                self.log_delim()
            self.output.ed_timer('Evolution_evaluate')

            # update pareto front
            population = tools.selNSGA2(population + offspring, len(offspring))
            front.update(population)

            for individual in front:
                if best > individual:
                    best = individual
                    self.limit.set('stagnation', -1)

            # restart
            self.output.st_timer('Evolution_next', 'next')
            self.limit.increase('iteration')
            self.limit.increase('stagnation')
            if self.limit.get('stagnation') >= self.stagnation_limit:
                self.log_delim().output.log('Front:')
                for point in front:
                    self.output.log(str(point))

                front = tools.ParetoFront()
                points.append(best)
                best = root

                self.limit.set('stagnation', 0)
                info = self.strategy.configure(self.limit.limits)
                self.output.debug(3, 1, 'configure: ' + str(info))
                population = [root]
                pop = self.strategy.breed(population)
                offspring = [creator.Individual(ind.backdoor) for ind in pop]

                # create new log file
                if not self.limit.exhausted():
                    self.touch_log().log_info().log_delim()
            else:
                info = self.strategy.configure(self.limit.limits)
                self.output.debug(3, 1, 'configure: ' + str(info))
                pop = self.strategy.breed(population)
                offspring = [creator.Individual(ind.backdoor) for ind in pop]
            self.output.ed_timer('Evolution_next')

            self.limit.set('time', now() - timestamp)
            self.output.ed_timer('Evolution_iteration_%d' % it)

        if root > best:
            self.log_delim().output.log('Front:')
            for point in front:
                self.output.log(str(point))

            points.append(best)

        self.output.ed_timer(self.name)
        return points

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy,
            'Weights: %s' % str(self.weights),
            'Stagnations: %d' % self.stagnation_limit,
        ]))


__all__ = [
    'MultiEvolution'
]
