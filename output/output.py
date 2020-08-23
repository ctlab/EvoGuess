from .tools import *

from os import makedirs
from os.path import join
from typing import Iterable


class Output:
    def __init__(self, **kwargs):
        self.path = kwargs['path']
        if isinstance(self.path, list):
            self.path = join(*self.path)
        self.largs = kwargs.get('largs', {})
        self.dargs = kwargs.get('dargs', {})
        self.targs = kwargs.get('targs', {})

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.size = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

        self.logger = logger(self.rank, **self.largs)
        self.debugger = debugger(self.rank, **self.dargs)
        self.timer = timer(self.rank, **self.targs)

    def open(self, **kwargs):
        if self.rank == 0:
            makedirs(self.path, exist_ok=True)
            self.logger.set_out(join(self.path, 'log'))

        if self.size > 1:
            self.comm.bcast(True, root=0)
        self.debugger.set_out(join(self.path, 'debug_%d' % self.rank))

        return self

    def log(self, *strs: Iterable[str]):
        self.logger.write(*strs)
        return self

    def debug(self, verb: int, level: int, *strs: Iterable[str]):
        self.debugger.write(verb, level, *strs)
        return self

    def st_timer(self, name: str, group: str):
        self.timer.start(name, group)

    def ed_timer(self, name: str):
        self.timer.end(name)


__all__ = [
    'Output',
    'Iterable',
]
