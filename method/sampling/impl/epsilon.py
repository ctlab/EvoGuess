from ..sampling import *
from math import log, sqrt, ceil


class Epsilon(Sampling):
    def __init__(self, instance, mn, mx, step, eps, delta=0.05):
        self.delta = delta
        self.min, self.max = mn, mx
        self.step, self.eps = step, eps
        self.name = 'Sampling: Epsilon (%d..%d, eps: %.2f, delta: %.2f)' % (mn, mx, eps, delta)
        super().__init__(instance)

    def _n_e_d(self, values):
        n = len(values)
        e = sum(values) / n
        d = sum([(value - e) ** 2 for value in values]) / (n - 1)
        return n, e, d

    def _get_eps(self, values):
        n, e, d = self._n_e_d(values)
        return sqrt(d / (self.delta * n)) / e

    def get_count(self, backdoor: Backdoor, values=()):
        count = len(values)
        bd_count = self.base ** len(backdoor)
        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if self._get_eps(values) > self.eps:
                bound = min(count + self.step, self.max, bd_count)
                return bound - count
        return 0

    def get_max(self) -> Tuple[int, int]:
        return self.max, ceil(log(self.max) / log(self.base))


__all__ = [
    'Epsilon'
]
