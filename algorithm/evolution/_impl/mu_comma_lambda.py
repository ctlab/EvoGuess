from ..evolution import *


class MuCommaLambda(Evolution):
    def __init__(self, mu, lmbda, *args, **kwargs):
        self.population_size = lmbda
        self.mu, self.lmbda = mu, lmbda
        self.name = 'Algorithm: Evolution (%d, %d)' % (mu, lmbda)
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        return list(map(self.mutation.mutate, selected))

    def join(self, parents: Population, children: Population):
        return sorted(children)[:self.mu]


__all__ = [
    'MuCommaLambda'
]
