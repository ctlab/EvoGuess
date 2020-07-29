import math


class Estimation:
    def __init__(self, cases, value):
        self.value = value
        self.cases = cases
        self.from_cache = False

    def value_sd(self):
        n, e, e2 = len(self.cases), 0., 0.
        for case in self.cases:
            e += case.value
            e2 += case.value ** 2

        d = (e2 / n) - (e / n) ** 2
        return math.sqrt(d)

    def __len__(self):
        return len(self.cases)


__all__ = [
    'Estimation'
]
