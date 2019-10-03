from ..sampling import *


class Const(Sampling):
    def __init__(self, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count

    def __len__(self):
        return self.count


__all__ = [
    'Const'
]
