from .backdoor import *


class Interval:
    def __init__(self, st, length):
        self.st, self.end = st, st + length
        self.list = range(st, self.end)

        if self.st <= 0:
            raise Exception('Interval contains negative numbers or zero')

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return '%s..%s' % (self.st, self.end - 1)

    def values(self, **kwargs):
        return get_values(self.list, **kwargs)

    def to_backdoor(self):
        return Backdoor(self.list)


__all__ = [
    'Interval'
]
