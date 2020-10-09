from ..evolution import *


class MuCommaLambda(Evolution):
    def __init__(self,
                 mu: int,
                 lmbda: int,
                 limit,
                 method,
                 output,
                 mutation,
                 selection
                 ):
        self.mu, self.lmbda = mu, lmbda
        self.name = 'Algorithm: Evolution (%d, %d)' % (mu, lmbda)
        super().__init__(limit, method, output, mutation, selection)

    def tweak(self, selected: Population):
        return list(map(self.mutation.mutate, selected))

    def join(self, parents: Population, children: Population):
        return sorted(children)[:self.mu]


__all__ = [
    'MuCommaLambda'
]
