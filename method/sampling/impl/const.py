from ..sampling import *


class Const(Sampling):
    def __init__(self, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count

    def get_count(self, backdoor: Backdoor, sample=()):
        count = min(self.count, 2 ** len(backdoor))
        return max(0, count - len(sample))


__all__ = [
    'Const'
]
