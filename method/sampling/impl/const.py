from ..sampling import *
from math import log2, ceil


class Const(Sampling):
    def __init__(self, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count

    def get_count(self, backdoor: Backdoor, values=()):
        count = min(self.count, 2 ** len(backdoor))
        return max(0, count - len(values))

    def get_max(self) -> Tuple[int, int]:
        return self.count, ceil(log2(self.count))


__all__ = [
    'Const'
]
