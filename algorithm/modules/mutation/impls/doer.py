from ..mutation import *


class Doer(Mutation):
    name = 'Mutation: Doer'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aperi_const = 1.202056

    def __get_alpha(self, size):
        half_size = size // 2
        if half_size == 1:
            return 1

        l, p, r = 0., self.rs.rand(), 0.
        for i in range(half_size):
            l = r
            r += (1. / (self.aperi_const * ((i + 1) ** 3)))
            if l <= p < r:
                return i + 1

        return half_size

    def mutate(self, i: Individual) -> Individual:
        v = i.backdoor.get_mask()
        p = self.__get_alpha(len(v)) / len(v)

        while True:
            distribution = self.rs.rand(len(v))
            if p > min(distribution):
                break

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Individual(i.backdoor.get_copy(v))


__all__ = ['Doer']
