from ..crossover import *


class Uniform(Crossover):
    name = 'Crossover: Uniform'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p = float(kwargs['p'])

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        vbd, wbd = i1.backdoor, i2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        distribution = self.rs.rand(len(v))
        for i in range(len(v)):
            if self.p >= distribution[i]:
                v[i], w[i] = w[i], v[i]

        return Individual(vbd.get_copy(v)), Individual(wbd.get_copy(w))

    def __str__(self):
        return ''.join([
            self.name, ' (p: %.2f' % self.p,
            ', seed: %s)' % self.seed if self.seed else ')'
        ])


__all__ = ['Uniform']
