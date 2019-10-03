from ..algorithm import *

from time import time as now


class Evolution(Algorithm):
    name = 'Algorithm: Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strategy = kwargs['strategy']

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.size = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

    def start(self, backdoor: Backdoor) -> List[Individual]:
        timestamp = now()
        self.output.debug(0, 0, 'Evolution start on %d nodes' % self.size)

        if self.rank == 0:
            points = []
            self.log_info().log_delim()
            self.limit.set('stagnation', 1)

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
                for i in population:
                    key = str(i.backdoor)
                    if key in self.values:
                        value, _ = self.values[key]
                        self.log_hashed(i.backdoor, value).log_delim()
                    else:
                        count = len(self.sampling)
                        self.log_run(i.backdoor, count)
                        value = self.__predict(i.backdoor, count)
                        self.limit.increase('predictions')
                        self.values[key] = value, count
                        i.estimate(value)
                        self.log_end(value).log_delim()

                        if best > i:
                            best = i
                            self.limit.set('stagnation', -1)

                population = self.strategy.breed(population)
                self.limit.set('time', now() - timestamp)
                # todo: restarts
                self.limit.increase('stagnation')
                self.limit.increase('iterations')

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
                self.predictor.predict(backdoor, count)

    def __predict(self, backdoor, count):
        if self.size > 1:
            self.output.debug(2, 1, 'Sending backdoor... %s' % backdoor)
            self.comm.bcast([count] + backdoor.snapshot(), root=0)

        return self.predictor.predict(backdoor, count)

    def __restart(self, i):
        return [i] * len(self.strategy)

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy
        ]))


__all__ = [
    'Evolution'
]
