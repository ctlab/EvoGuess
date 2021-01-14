from ..sampling import *
from math import log, floor


class Const(Sampling):
    def __init__(self, instance, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count
        super().__init__(instance)

    def get_count(self, backdoor: Backdoor, values=()):
        count = min(self.count, 2 ** len(backdoor))
        return max(0, count - len(values))

    def get_max(self) -> Tuple[int, int]:
        return self.count, floor(log(self.count) / log(self.base))


__all__ = [
    'Const'
]
