import threading


def logger(prefix=''):
    try:
        from mpi4py import MPI
        rank = MPI.COMM_WORLD.Get_rank()
        return Logger(prefix) if rank == 0 else LoggerStub()
    except ModuleNotFoundError:
        return Logger(prefix)


class Logger:
    def __init__(self, prefix=''):
        self.path = None
        self.prefix = prefix
        self.lock = threading.Lock()
        if len(prefix): self.prefix += ' '

    def set_out(self, path):
        self.path = path
        open(path, 'w+').close()

    def write(self, *strs):
        if not len(strs): return

        self.lock.acquire()
        if self.path:
            with open(self.path, "a") as f:
                [f.write(self.__line(s)) for s in strs]
        else:
            [print(self.__line(s)) for s in strs]
        self.lock.release()

    def __line(self, s):
        return '%s%s\n' % (self.prefix, s.strip())


class LoggerStub:
    def __init__(self, prefix=''):
        pass

    def set_out(self, path):
        pass

    def write(self, *strs):
        pass


__all__ = [
    'logger',
]
