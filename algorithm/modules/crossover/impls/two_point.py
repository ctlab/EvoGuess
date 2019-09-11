from ..crossover import *


class TwoPointCrossover(Crossover):
    name = 'Crossover: two-point'

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        vbd, wbd = i1.backdoor, i2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        a, b = self.rs.randint(len(v)), self.rs.randint(len(v))
        a, b = min(a, b), max(a, b)

        for i in range(a, b):
            v[i], w[i] = w[i], v[i]

        return Individual(vbd.get_copy(v)), Individual(wbd.get_copy(w))


__all__ = ['TwoPointCrossover']
