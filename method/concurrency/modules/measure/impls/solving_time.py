from ..measure import *


class SolvingTime(Measure):
    name = 'Measure: SolvingTime'

    def get(self, result: Result):
        return result.time


__all__ = [
    'SolvingTime'
]
