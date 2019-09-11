from ..mutation import *


class UniformMutation(Mutation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = kwargs.get('scale') or 1.

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

    def __str__(self):
        return 'Mutation: uniform with scale p = %.2f' % self.scale


__all__ = ['UniformMutation']
