from .models import Task, Result

import signal
from typing import List


class Concurrency:
    name = 'Concurrency'

    def __init__(self, **kwargs):
        self.solver = kwargs['solver']
        self.propagator = kwargs['propagator']

        self.threads = kwargs['threads']
        self.processes = kwargs['threads']
        self.keep = kwargs.get('keep', False)

        signal.signal(signal.SIGINT, self.__signal_handler)

    def __signal_handler(self, signum: int, frame):
        self.terminate()
        exit(signum)

    def set_complexity(self, complexity=1):
        processes, remainder = divmod(self.threads, complexity)

        if processes == 0 or remainder != 0:
            raise Exception('Incorrect complexity or number of threads')
        elif processes != self.processes:
            self.processes = processes

    def single(self, task: Task, **kwargs) -> Result:
        raise NotImplementedError

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        raise NotImplementedError

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            'Keep: %d' % self.keep,
            'Threads: %d' % self.threads,
            'Processes: %d' % self.processes,
            'Solver: %s' % self.solver,
            'Propagator: %s' % self.propagator,
        ]))


__all__ = [
    'List',
    'Task',
    'Result',
    'Concurrency'
]
