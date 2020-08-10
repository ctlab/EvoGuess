from ..measure import *


class Conflicts(Measure):
    key = 'conflicts'
    name = 'Measure: Conflicts'

    def get(self, result: Result):
        return max(1, result.stats.get(self.key, 0))


__all__ = [
    'Conflicts'
]
