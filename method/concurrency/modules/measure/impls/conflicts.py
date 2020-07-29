from ..measure import *


class Conflicts(Measure):
    key = 'conflicts'
    name = 'Corrector: Conflicts'

    def get(self, result: Result):
        return result.stats[self.key] if self.key in result.stats else 0


__all__ = [
    'Conflicts'
]
