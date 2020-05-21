from numpy.random.mtrand import RandomState

from algorithm.models.individual import Individual


class Mutation:
    name = 'Mutation'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed')
        self.rs = RandomState(seed=self.seed)

    def mutate(self, i: Individual) -> Individual:
        raise NotImplementedError

    def configure(self, limits):
        pass

    def __str__(self):
        return self.name + (' (seed: %s)' % self.seed if self.seed else '')


__all__ = [
    'Mutation',
    'Individual'
]
