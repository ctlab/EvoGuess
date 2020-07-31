from ..subset import *
from numpy.random import RandomState
from method.instance.models.var import Backdoor


class Random(Subset):
    def __init__(self, **kwargs):
        self.size = kwargs['size']
        self.rs = RandomState(kwargs.get('seed'))

    def generate(self, backdoor: Backdoor):
        size = min(self.size, len(backdoor))
        variables = backdoor.snapshot()
        return Backdoor(self.rs.choice(variables, size, replace=False))


__all__ = [
    'Random'
]
