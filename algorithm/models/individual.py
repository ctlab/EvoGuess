from numpy import sign
from typing import List

from method.instance.models.var import Backdoor


class Individual:
    def __init__(self, backdoor: Backdoor):
        self.eps = float('inf')
        self.value = float('inf')
        self.backdoor = backdoor

    def set(self, value, eps=None):
        self.value = value
        if eps is not None:
            self.eps = eps
        return self

    def compare(self, other):
        try:
            vs = int(sign(self.value - other.value))
        except ValueError:
            vs = 0

        return vs or len(other) - len(self)

    def __len__(self):
        return len(self.backdoor)

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __str__(self):
        return '%s by %.7g' % (self.backdoor, self.value)


Population = List[Individual]

__all__ = [
    'Individual',
    'Population'
]
