import math


class Estimation:
    def __init__(self, cases, value):
        self.value = value
        self.cases = cases
        self.from_cache = False
        self.values = [case.value for case in self.cases]

    def __ned(self, values):
        n = len(values)
        e = sum(values) / n
        d = sum([(value - e) ** 2 for value in values]) / (n - 1)
        return n, e, d

    def eps(self, delta=0.05):
        n, e, d = self.__ned(self.values)
        return math.sqrt(d / (delta * n)) / e

    def value_sd(self):
        _, _, d = self.__ned(self.values)
        return math.sqrt(d)

    def __len__(self):
        return len(self.cases)


__all__ = [
    'Estimation'
]
