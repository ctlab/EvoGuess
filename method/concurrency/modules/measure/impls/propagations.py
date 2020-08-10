from ..measure import *


class Propagations(Measure):
    key = 'propagations'
    name = 'Measure: Propagations'

    def get(self, result: Result):
        return max(1, result.stats.get(self.key, 0))


__all__ = [
    'Propagations'
]
