from ..sampling import *


class Const(Sampling):
    def __init__(self, count: int):
        self.count = count

    def __len__(self):
        return self.count


__all__ = [
    'Const'
]
