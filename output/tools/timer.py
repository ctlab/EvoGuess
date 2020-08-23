import threading

from time import time as now
from datetime import datetime as dt


def timer(rank, tall=False, prefix=''):
    return Timer(prefix) if tall or rank == 0 else TimerStub()


class Timer:
    def __init__(self, prefix=''):
        self.path = None
        self.prefix = prefix
        if len(prefix): self.prefix += ' '

        self.stack = []
        self.last = None

    def set_out(self, path):
        self.path = path
        open(path, 'w+').close()

    def start(self, name, group):
        if self.path:
            self.__delay()
            res = '%s(%s) %s' % (self.prefix, dt.today(), '-' * len(self.stack))
            with open(self.path, 'a') as f:
                f.write("%s %s (%s)\n" % (res, name, group))

            self.stack.append((name, group, now()))

    def end(self, name):
        if self.path:
            assert len(self.stack) > 0, "Stack len error"
            el = self.stack.pop()
            assert el[0] == name, "Stack name error"

            self.last = now()
            res = '%s(%s) %s' % (self.prefix, dt.today(), '-' * len(self.stack))
            with open(self.path, 'a') as f:
                f.write("%s %s with %.2f\n" % (res, name, self.last - el[2]))

    def __delay(self):
        if self.last is not None:
            delay = now() - self.last
            if delay >= 0.1:
                with open(self.path, 'a') as f:
                    res = '%s(%s) %s' % (self.prefix, dt.today(), '-' * len(self.stack))
                    f.write("%s delay (delay)\n" % res)
                    f.write("%s delay with %.2f\n" % (res, now() - self.last))

        self.last = None



class TimerStub:
    def set_out(self, path):
        pass

    def start(self, name, group):
        pass

    def end(self, name):
        pass


__all__ = [
    'timer',
    'Timer',
    'TimerStub'
]
