from ..mutation import *

from math import pow


class Doer(Mutation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.beta = kwargs.get('beta', 3)
        self.name = 'Mutation: Doer (beta: %d)' % self.beta

    def __get_alpha(self, size):
        bound = size // 2 + 1
        if bound < 3:
            return 1

        ll, p, rr = 0., self.rs.rand(), 0.
        c = sum(1. / pow(i, self.beta) for i in range(1, bound))
        for k in range(1, bound):
            ll = rr
            rr += (1. / (c * pow(k, self.beta)))
            if ll <= p < rr:
                return k

        return bound - 1

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
