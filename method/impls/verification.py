from ..method import *
from ..concurrency import Task, Result

from copy import copy
from time import time as now
from numpy import concatenate


class Verification(Method):
    name = 'Method: Verification'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chunk_size = kwargs['chunk_size']

    def __get_next_values(self, values):
        new_values, i = copy(values), len(values) - 1
        while i >= 0 and new_values[i] != 0:
            new_values[i] = 0
            i -= 1

        if i < 0:
            return None
        else:
            new_values[i] = 1
            return new_values

    def __solve(self, chunk):
        self.output.debug(1, 0, 'Solve chunk with size: %d' % len(chunk))
        timestamp = now()
        results = self.concurrency.solve(chunk, **self.kwargs)
        time = now() - timestamp

        self.output.debug(1, 0, 'Has been solved %d tasks by %.2f seconds' % (len(results), time))
        if len(chunk) != len(results):
            self.output.debug(0, 0, 'Warning! len(chunk) != len(results)')

        return results

    def run(self, backdoor: Backdoor, **kwargs) -> Estimation:
        count = 2 ** len(backdoor)
        self.log_run(backdoor, count)
        variables = backdoor.snapshot()
        instance, rs = self.kwargs['instance'], self.kwargs['rs']

        # init
        if instance.has_values():
            timestamp = now()
            task = Task(0, proof=True, secret_key=instance.secret_key.values(rs=rs))
            result = self.concurrency.single(task, **self.kwargs)
            self.output.debug(1, 0, 'Init case solved by %.2f seconds' % (now() - timestamp))
        else:
            result = Result(0, True, 0, {}, [])
            self.output.debug(1, 0, 'Skip init phase')

        mpi_count, remainder = divmod(count, self.size)
        st = mpi_count * self.rank + min(self.rank, remainder)
        mpi_count += 1 if remainder > self.rank else 0

        values = [1 if st & (1 << i) else 0 for i in range(len(backdoor))][::-1]

        timestamp = now()
        cases, chunk = [], []
        for i in range(st, st + mpi_count):
            assert values is not None
            assumption = [x if values[j] else -x for j, x in enumerate(variables)]
            chunk.append(Task(i, bd=assumption, **instance.values(solution=result.solution)))
            values = self.__get_next_values(values)

            if len(chunk) >= self.chunk_size:
                results = self.__solve(chunk)
                cases.extend(results)
                chunk = []

        if len(chunk) > 0:
            results = self.__solve(chunk)
            cases.extend(results)

        if self.size > 1:
            g_cases = self.comm.gather(cases, root=0)

            if self.rank == 0:
                self.output.debug(2, 1, 'Been gathered cases from %d nodes' % len(cases))
                cases = concatenate(g_cases)

        value, t_value = 0, 0
        time = now() - timestamp
        if self.rank == 0:
            stat = {'IND': 0, 'DET': 0}
            for case in cases:
                value += case.value
                t_value += case.time
                stat['IND' if case.status is None else 'DET'] += 1

            self.output.log(*list(map(str, cases)))
            self.output.log(str(stat).replace('\'', ''))
            self.output.debug(1, 0, 'Value: %.7g (%.7g)' % (value, t_value))
            self.output.log('Spent time: %.2f s' % time, 'End with value: %.7g' % value)

        return Estimation(cases, value)


__all__ = [
    'Verification'
]
