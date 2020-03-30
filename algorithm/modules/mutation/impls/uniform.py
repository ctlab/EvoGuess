from ..mutation import *


class Uniform(Mutation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = kwargs.get('scale', 1.)

        self.name = 'Mutation: Uniform (scale: %.1f, seed: %s)' % (self.scale, self.seed)

    def mutate(self, i: Individual) -> Individual:
        v = i.backdoor.get_mask()
        p = self.scale / len(v)

        while True:
            distribution = self.rs.rand(len(v))
            if p > min(distribution):
                break

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Individual(i.backdoor.get_copy(v))


__all__ = ['Uniform']
