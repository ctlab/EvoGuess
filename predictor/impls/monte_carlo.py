from ..predictor import *

from time import time as now
from numpy import concatenate
from pickle import dumps, loads


class MonteCarlo(Predictor):
    name = 'Predictor: MonteCarlo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method = kwargs['method']

    def predict(self, backdoor: Backdoor, **kwargs) -> int:
        count = kwargs.pop('count')
        mpi_count, remainder = divmod(count, self.size)
        mpi_count += 1 if remainder > self.rank else 0

        timestamp = now()
        cases = self.method.compute(backdoor, [], mpi_count, **self.kwargs, **kwargs)
        if self.size > 1:
            self.output.debug(2, 1, 'Gathering cases from %d nodes...' % self.size)
            g_cases = self.comm.gather(dumps(cases), root=0)

            if self.rank == 0:
                self.output.debug(2, 1, 'Been gathered cases from %d nodes' % self.size)
                cases = concatenate([loads(g_case) for g_case in g_cases])

        value, time = 0, now() - timestamp
        if self.rank == 0:
            estimation = self.method.estimate(backdoor, cases, **self.kwargs)
            self.log_info(cases, estimation, time)
            value = estimation.value

        return value

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.method,
        ]))


__all__ = [
    'MonteCarlo'
]
