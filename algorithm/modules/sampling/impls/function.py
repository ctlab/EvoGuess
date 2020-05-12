from ..sampling import *


class Function(Sampling):
    name = 'Sampling: Function'

    def __init__(self, f):
        self.f = f

    def get_size(self, backdoor: Backdoor):
        return self.f(backdoor)


__all__ = [
    'Function'
]
