from ..method import *

from time import time as now
from numpy import concatenate
from pickle import dumps, loads


class MonteCarlo(Method):
    name = 'Method: MonteCarlo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function = kwargs['function']

    def run(self, backdoor: Backdoor, **kwargs) -> Estimation:
        count = kwargs.pop('count')
        self.log_run(backdoor, count)
        mpi_count, remainder = divmod(count, self.size)
        mpi_count += 1 if remainder > self.rank else 0

        timestamp = now()
        cases = self.function.evaluate(backdoor, [], mpi_count, **self.kwargs, **kwargs)
        if self.size > 1:
            self.output.debug(2, 1, 'Gathering cases from %d nodes...' % self.size)
            g_cases = self.comm.gather(dumps(cases), root=0)

            if self.rank == 0:
                self.output.debug(2, 1, 'Been gathered cases from %d nodes' % self.size)
                cases = concatenate([loads(g_case) for g_case in g_cases])

        value, time = 0, now() - timestamp
        if self.rank == 0:
            info = self.function.calculate(backdoor, cases, **self.kwargs)
            self.log_end(cases, info, time)
            value = info.value
        else:
            cases = []
        
        return Estimation(cases, value)

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.function,
        ]))


__all__ = [
    'MonteCarlo'
]
