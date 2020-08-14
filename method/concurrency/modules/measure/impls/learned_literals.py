from ..measure import *


class LearnedLiterals(Measure):
    key = 'learned_literals'
    name = 'Measure: Learned Literals'

    def get(self, result: Result):
        return max(1, result.stats.get(self.key, 0))


__all__ = [
    'LearnedLiterals'
]
