from .models import *

from enum import Enum
from typing import List
from method.instance.models.var import Backdoor


class BTypes(Enum):
    EXIT = 0
    TOUCH = 1
    ESTIMATE = 2


class Algorithm:
    name = 'Algorithm'

    def __init__(self, **kwargs):
        self.limit = kwargs['limit']
        self.output = kwargs['output']
        self.method = kwargs['method']
        self.sampling = kwargs['sampling']

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.size = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

    def process(self, backdoor: Backdoor) -> List[Individual]:
        raise NotImplementedError

    def start(self, backdoor: Backdoor) -> List[Individual]:
        self.output.debug(0, 0, '%s start on %d nodes' % (self.name, self.size))

        if self.rank == 0:
            points = self.process(backdoor)
            
            for i in range(1, self.size):
                self.comm.send([BTypes.EXIT.value], dest=i)

            self.log_delim()
            self.output.log('Points:')
            for point in points:
                self.output.log(str(point))

            return points
        else:
            while True:
                array = self.comm.recv(None, source=0)
                try:
                    b_type = BTypes(array[0])
                    if b_type is BTypes.EXIT:
                        self.output.debug(2, 1, 'Been received \'exit\'')
                        return []
                    elif b_type is BTypes.TOUCH:
                        self.output.debug(2, 1, 'Been received \'touch\'')
                        self.output.touch()
                    elif b_type is BTypes.ESTIMATE:
                        count, variables = array[1], array[2:]
                        backdoor = Backdoor(variables)
                        self.output.debug(2, 1, 'Been received backdoor: %s' % backdoor)
                        self.method.estimate(backdoor, count=count)
                except ValueError:
                    self.output.debug(2, 1, 'Been received unknown Btype')
                    return []

    def predict(self, backdoor, count):
        for i in range(1, self.size):
            self.output.debug(2, 1, 'Sending to %d backdoor... %s' % (i, backdoor))
            self.comm.send([BTypes.ESTIMATE.value, count] + backdoor.snapshot(), dest=i)

        return self.method.estimate(backdoor, count=count)

    def touch_log(self):
        self.output.touch()
        for i in range(1, self.size):
            self.comm.send([BTypes.TOUCH.value], dest=i)

        return self

    def log_info(self):
        self.output.log('\n'.join('-- ' + s for s in str(self).split('\n')))
        return self

    def log_delim(self):
        self.output.log('------------------------------------------------------')
        return self

    def log_it_header(self, it, more=''):
        self.output.log('Iteration: %d%s' % (it, ' (%s)' % more if len(more) else ''))
        return self

    def log_run(self, backdoor, count):
        self.output.log('Run estimation on backdoor: %s' % backdoor, 'With %d cases:' % count)
        return self

    def log_end(self, value):
        self.output.log('End estimation with value: %.7g' % value)
        return self

    def log_hashed(self, backdoor, value):
        self.output.log('Hashed backdoor: %s' % backdoor, 'With value: %.7g\n' % value)
        return self

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.method,
            self.sampling
        ]))


__all__ = [
    'List',
    'BTypes',
    'Backdoor',
    'Algorithm',
    'Individual'
]
