from .instance.models.var import Backdoor

from time import time as now
from numpy import concatenate


class Predictor:
    name = 'Predictor'

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.method = kwargs['method']
        self.output = kwargs['output']

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            self.size = self.comm.Get_size()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

    def predict(self, backdoor: Backdoor, count: int, **kwargs) -> int:
        mpi_count, remainder = divmod(count, self.size)
        mpi_count += 1 if remainder > self.rank else 0

        timestamp = now()
        cases = self.method.compute(backdoor, [], mpi_count, **self.kwargs, **kwargs)
        if self.size > 1:
            g_cases = self.comm.gather(cases, root=0)

            if self.rank == 0:
                self.output.debug(2, 1, "Been gathered cases from %d nodes" % len(cases))
                cases = concatenate(g_cases)

        value, time = 0, now() - timestamp
        if self.rank == 0:
            estimation = self.method.estimate(backdoor, cases, **self.kwargs)
            self.__log(cases, estimation, time)
            value = estimation.value

        return value

    def __log(self, cases, estimation, time):
        for case in cases:
            self.output.log(str(case))

        self.output.log(str(estimation))
        self.output.log('Spent time: %.2f s' % time)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.kwargs['instance'],
            self.method,
        ]))


__all__ = [
    'Predictor'
]
