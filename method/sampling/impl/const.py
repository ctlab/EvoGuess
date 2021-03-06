from ..sampling import *

import re
from math import log, floor


class Const(Sampling):
    def __init__(self, instance, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count
        super().__init__(instance)

    def get_count(self, backdoor: Backdoor, values=()):
        count = min(self.count, self.base ** len(backdoor))
        return max(0, count - len(values))

    def get_max(self) -> Tuple[int, int]:
        return self.count, floor(log(self.count) / log(self.base))

    @staticmethod
    def parse(params):
        args = re.findall(r'^(\d+)$', params)
        return {
            'count': int(args[0])
        } if len(args) else None


__all__ = [
    'Const'
]
