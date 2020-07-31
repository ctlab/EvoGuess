from ..measure import *


class Propogations(Measure):
    key = 'propagations'
    name = 'Corrector: Propagations'

    def get(self, result: Result):
        return max(1, result.stats.get(self.key, 0))


__all__ = [
    'Propogations'
]
