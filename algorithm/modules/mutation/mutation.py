from numpy.random.mtrand import RandomState

from algorithm.models.individual import Individual


class Mutation:
    name = 'Mutation'

    def __init__(self, **kwargs):
        self.rs = RandomState(seed=kwargs.get('seed'))

    def mutate(self, i: Individual) -> Individual:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Mutation',
    'Individual'
]
