from output.module.logger import get_logger as gl
from output.module.debugger import get_debugger as gdb


class Comm:
    def __init__(self, **kwargs):
        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

        path = kwargs['log']
        self.logger = gl(path if self.rank == 0 else '')
        paths, verb = kwargs['debug']
        self.debugger = gdb(paths[self.rank], verb)

    def log(self, *strs):
        self.logger.write(*strs)

    def d_log(self, *strs):
        self.logger.deferred_write(*strs)

    def debug(self, verb, level, *strs):
        self.debugger.write(verb, level, *strs)

    def d_debug(self, verb, level, *strs):
        self.debugger.deferred_write(verb, level, *strs)
