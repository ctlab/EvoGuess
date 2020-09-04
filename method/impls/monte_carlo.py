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

        timestamp = now()
        real_count = 2 ** len(backdoor)
        if self.function.type == 'gad' and real_count > count:
            self.log_run(backdoor, count)
            mpi_count, remainder = divmod(count, self.size)
            mpi_count += 1 if remainder > self.rank else 0

            self.output.st_timer('Evaluate', 'evaluate')
            cases = self.function.evaluate(backdoor, [], mpi_count, **self.kwargs, **kwargs)
            self.output.ed_timer('Evaluate')
        else:
            self.log_run(backdoor, real_count)
            mpi_count, remainder = divmod(real_count, self.size)
            st = mpi_count * self.rank + min(self.rank, remainder)
            mpi_count += 1 if remainder > self.rank else 0

            self.output.st_timer('Evaluate', 'evaluate')
            cases = self.function.verify(backdoor, mpi_count, st, **self.kwargs, **kwargs)
            self.output.ed_timer('Evaluate')

        g_step = 200
        self.output.st_timer('Evaluate_await', 'await')
        if self.size > 1:
            self.output.debug(2, 1, 'Gathering cases from %d nodes...' % self.size)
            all_cases = []

            g_count = self.comm.allgather(len(cases))
            self.output.debug(2, 1, 'Gather counts: %s' % g_count)
            g_sessions = max(len(range(0, count, g_step)) for count in g_count)

            for i in range(g_sessions):
                st = i * g_step
                g_cases = self.comm.gather(dumps(cases[st:st + g_step]), root=0)

                if self.rank == 0:
                    self.output.debug(2, 1, 'Been gathered cases from %d nodes' % self.size)
                    all_cases.extend(concatenate([loads(g_case) for g_case in g_cases]))
            cases = all_cases
        self.output.ed_timer('Evaluate_await')

        self.output.st_timer('Calculate', 'calculate')
        value, time = 0, now() - timestamp
        if self.rank == 0:
            info = self.function.calculate(backdoor, cases, **self.kwargs)
            self.output.st_timer('Calculate_log', 'log')
            self.log_end(cases, info, time)
            self.output.ed_timer('Calculate_log')
            value = info.value
        else:
            cases = []
        self.output.ed_timer('Calculate')

        return Estimation(cases, value)

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.function,
        ]))


__all__ = [
    'MonteCarlo'
]
