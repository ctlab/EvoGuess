from ..measure import *


class Propogations(Measure):
    key = 'propagations'
    name = 'Corrector: Propagations'

    def get(self, result: Result):
        return result.stats[self.key] if self.key in result.stats else 0


__all__ = [
    'Propogations'
]
