from ..method import *
from ..concurrency.models import Task

from copy import copy
from time import time as now


class SimpleVerification(Method):
    name = 'Method: Simple Verification'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chunk_size = kwargs['chunk_size']
        self.chunk_sorting = kwargs.get('chunk_sorting')

    def __get_chunk(self, count):
        values = [0] * count
        chunk = [values]
        while values is not None:
            values, i = copy(values), count - 1
            while i >= 0 and values[i] != 0:
                values[i] = 0
                i -= 1

            if i < 0:
                values = None
            else:
                values[i] = 1
                chunk.append(values)

        return chunk

    def run(self, backdoor: Backdoor, **kwargs) -> Estimation:
        count = 2 ** len(backdoor)
        if count >= self.chunk_size:
            raise Exception('Too much tasks')

        self.log_run(backdoor, count)
        variables = backdoor.snapshot()
        chunk = self.__get_chunk(len(backdoor))

        if self.chunk_sorting is not None:
            chunk = self.chunk_sorting.sort(chunk)

        tasks = []
        for i, values in enumerate(chunk):
            assert values is not None
            assumption = [x if values[j] else -x for j, x in enumerate(variables)]
            tasks.append(Task(i, bd=assumption, **kwargs))

        self.output.debug(1, 0, 'Solve chunk with size: %d' % len(tasks))
        timestamp = now()
        results = self.concurrency.solve(tasks, **self.kwargs)
        time = now() - timestamp

        self.output.debug(1, 0, 'Has been solved %d tasks by %.2f seconds' % (len(results), time))
        if len(tasks) != len(results):
            self.output.debug(0, 0, 'Warning! len(tasks) != len(results)')

        value, time = 0, now() - timestamp
        if self.rank == 0:
            stat = {'IND': 0, 'DET': 0}
            for case in results:
                value += case.time
                self.output.log(str(case))
                stat['IND' if case.status is None else 'DET'] += 1

            self.output.log(str(stat).replace('\'', ''))
            self.output.log('Spent time: %.2f s' % time, 'End with value: %.7g' % value)

        return Estimation(count, value)


__all__ = [
    'SimpleVerification'
]
