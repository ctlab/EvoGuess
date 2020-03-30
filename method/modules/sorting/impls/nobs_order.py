from ..sorting import *

from numpy import count_nonzero as cnz


def key_f(values):
    return abs(2 * cnz(values) - len(values))


class NobsOrder(Sorting):
    def sort(self, chunk: List[int]) -> List[int]:
        return sorted(chunk, key=key_f)


__all__ = [
    'NobsOrder'
]
