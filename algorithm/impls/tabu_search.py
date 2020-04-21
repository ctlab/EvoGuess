from ..algorithm import *

from time import time as now


class TabuSearch(Algorithm):
    name = 'Algorithm: Tabu Search'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tabu = set()

    def process(self, backdoor: Backdoor) -> List[Individual]:
        timestamp = now()

        trace = []
        self.log_info().log_delim()
        self.limit.set('upgrades', 0)

        root, count = Individual(backdoor), len(self.sampling)
        self.log_it_header(0, 'base').log_delim()
        estimation = self.predict(backdoor, count)
        best = root.set(estimation.value)
        trace.append(root)
        self.log_delim()

        center = best
        self.limit.set('iteration', 1)
        self.limit.set('time', now() - timestamp)
        while not self.limit.exhausted():
            it = self.limit.get('iteration')
            self.log_it_header(it).log_delim()

            # self.method.switch(population) # todo: integrate

            updated = False
            next_center = None
            for individual in self.neighbourhood(center):
                backdoor = individual.backdoor
                estimation = self.predict(backdoor, count)
                if not estimation.from_cache:
                    self.limit.increase('predictions')
                    individual.set(estimation.value)
                self.log_delim()

                if self.is_tabu(individual):
                    self.output.debug(1, 0, 'Backdoor %s in tabu list' % individual)
                elif center > individual:
                    updated = True
                    next_center = individual
                    break

            if updated:
                self.add_tabu(center)
                trace.append((center, next_center))
                center = next_center

                if best > center:
                    best = next_center
                    self.limit.increase('upgrades')
            else:
                center, next_center = trace.pop()
                self.remove_tabu(center)
                self.add_tabu(next_center)

            self.limit.increase('iteration')
            self.limit.set('time', now() - timestamp)

        return [best]

    def is_tabu(self, i):
        return str(i.backdoor) in self.tabu

    def add_tabu(self, i):
        self.tabu.add(str(i.backdoor))

    def remove_tabu(self, i):
        self.tabu.remove(str(i.backdoor))

    def neighbourhood(self, i):
        for j in range(i.backdoor.length):
            v = i.backdoor.get_mask()
            v[j] = not v[j]
            yield Individual(i.backdoor.get_copy(v))


__all__ = [
    'TabuSearch'
]
