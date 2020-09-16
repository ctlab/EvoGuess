from ..sampling import *


class Function(Sampling):
    def __init__(self, f):
        self.f = f
        self.name = 'Sampling: Function (%d..%d)' % (f([]), f([0] * 50))

    def get_size(self, backdoor: Backdoor):
        return self.f(backdoor)

    def analyse(self, population):
        pass

__all__ = [
    'Function'
]
