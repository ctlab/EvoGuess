from ..evolution import *
import re


class MuPlusLambda(Evolution):
    def __init__(self, mu, lmbda, *args, **kwargs):
        self.population_size = lmbda
        self.mu, self.lmbda = mu, lmbda
        self.name = 'Algorithm: Evolution (%d + %d)' % (mu, lmbda)
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        return list(map(self.mutation.mutate, selected))

    def join(self, parents: Population, children: Population):
        mu_parents = sorted(parents)[:self.mu]
        lmbda_children = sorted(children)[:self.lmbda]
        return mu_parents + lmbda_children

    @staticmethod
    def parse(params):
        args = re.findall(r'(\d+)\+(\d+)', params)
        return {
            'mu': int(args[0][0]),
            'lmbda': int(args[0][1])
        } if len(args) else None


__all__ = [
    'MuPlusLambda'
]
