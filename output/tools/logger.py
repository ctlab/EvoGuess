import threading


def logger(rank, prefix=''):
    return Logger(prefix) if rank == 0 else LoggerStub()


class Logger:
    def __init__(self, prefix=''):
        self.path = None
        self.prefix = prefix
        if len(prefix): self.prefix += ' '

    def set_out(self, path):
        self.path = path
        open(path, 'w+').close()

    def write(self, *strs):
        if not len(strs): return

        if self.path:
            with open(self.path, 'a') as f:
                [f.write(self.__line(s)) for s in strs]
        else:
            [print(self.__line(s)) for s in strs]

    def __line(self, s):
        return '%s%s\n' % (self.prefix, s.strip())


class LoggerStub:
    def set_out(self, path):
        pass

    def write(self, *strs):
        pass


__all__ = [
    'logger',
    'Logger',
    'LoggerStub'
]
