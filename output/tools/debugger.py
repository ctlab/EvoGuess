import threading

from datetime import datetime as dt


def debugger(verb=0, prefix=''):
    try:
        from mpi4py import MPI
        rank = MPI.COMM_WORLD.Get_rank()
        return Debugger(verb, prefix) if rank == 0 else DebuggerStub()
    except ModuleNotFoundError:
        return Debugger(verb, prefix)


class Debugger:
    def __init__(self, verb=0, prefix=''):
        self.path = None
        self.verb = verb
        self.prefix = prefix
        self.lock = threading.Lock()
        if len(prefix): self.prefix += ' '

    def set_out(self, path):
        self.path = path
        open(path, 'w+').close()

    def write(self, verb, lvl, *strs):
        if self.verb < verb:
            return

        self.lock.acquire()
        if self.path:
            with open(self.path, "a") as f:
                [f.write(self.__line(lvl, s)) for s in strs]
        else:
            [print(self.__line(lvl, s)) for s in strs]
        self.lock.release()

    def __line(self, lvl, s):
        res = '%s(%s)' % (self.prefix, dt.today())
        if lvl > 0:
            res = '%s %s' % (res, '--' * lvl)
        return '%s %s\n' % (res, s.strip())


class DebuggerStub:
    def __init__(self):
        pass

    def set_out(self, path):
        pass

    def write(self, verb, lvl, *strs):
        pass


__all__ = [
    'debugger',
]
