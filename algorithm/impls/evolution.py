from ..algorithm import *

from time import time as now


class Evolution(Algorithm):
    name = 'Algorithm: Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strategy = kwargs['strategy']
        self.stagnation_limit = kwargs['stagnation_limit']

    def start(self, backdoor: Backdoor) -> List[Individual]:
        self.output.debug(0, 0, 'Evolution start on %d nodes' % self.size)

        timestamp = now()
        if self.rank == 0:
            points = []
            self.log_info().log_delim()
            self.limit.set('stagnation', 0)

            root, count = Individual(backdoor), len(self.sampling)
            self.log_it_header(0, 'base').log_delim()
            self.log_run(backdoor, count)
            value = self.__predict(backdoor, count)
            self.values[str(backdoor)] = value, count
            best = root.estimate(value)
            self.log_end(value).log_delim()

            population = self.strategy.breed([best])
            self.limit.set('time', now() - timestamp)
            while not self.limit.exhausted():
                it = self.limit.get('iterations')
                self.log_it_header(it).log_delim()
                for ind in population:
                    key = str(ind.backdoor)
                    if key in self.values:
                        value, _ = self.values[key]
                        self.log_hashed(ind.backdoor, value).log_delim()
                    else:
                        count = len(self.sampling)
                        self.log_run(ind.backdoor, count)
                        value = self.__predict(ind.backdoor, count)
                        self.limit.increase('predictions')
                        self.values[key] = value, count
                        ind.estimate(value)
                        self.log_end(value).log_delim()

                        if best > ind:
                            best = ind
                            self.limit.set('stagnation', -1)

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
                        self.log_info().log_delim()
                else:
                    population = self.strategy.breed(population)

                self.limit.increase('iterations')
                self.limit.set('time', now() - timestamp)

            if self.size > 1:
                self.comm.bcast([-1], root=0)

            if best.value < root.value:
                points.append(best)
                print('Local: %s' % best)

            self.log_delim()
            self.output.log('Points:')
            for point in points:
                self.output.log(str(point))

            return points
        else:
            while True:
                array = self.comm.bcast(None, root=0)
                count, variables = array[0], array[1:]
                if count < 0:
                    return -1

                backdoor = Backdoor(variables)
                self.output.debug(2, 1, 'Been received backdoor: %s' % backdoor)
                self.predictor.predict(backdoor, count=count)

    def __predict(self, backdoor, count):
        if self.size > 1:
            self.output.debug(2, 1, 'Sending backdoor... %s' % backdoor)
            self.comm.bcast([count] + backdoor.snapshot(), root=0)

        return self.predictor.predict(backdoor, count=count)

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy,
            self.predictor
        ]))


__all__ = [
    'Evolution'
]
