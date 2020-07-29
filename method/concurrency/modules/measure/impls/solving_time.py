from ..measure import *


class SolvingTime(Measure):
    name = 'Corrector: SolvingTime'

    def get(self, result: Result):
        return result.time


__all__ = [
    'SolvingTime'
]
