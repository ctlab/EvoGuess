from typing import Tuple, Iterable

from algorithm.models.individual import Individual, Population


class Strategy:
    name = 'Strategy'

    def __init__(self, survived: int, **kwargs):
        self.survived = survived
        self.mutation = kwargs['mutation']
        self.selection = kwargs['selection']

    def breed(self, old: Population) -> Population:
        generator = self.selection.select(old, self.survived)
        parents, children = self.tweak(generator)
        return self.join(parents, children)

    def tweak(self, parents: Iterable[Individual]) -> Tuple[Population, Population]:
        raise NotImplementedError

    def join(self, parents: Population, children: Population) -> Population:
        return [*parents, *children]

    def __len__(self):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.mutation,
            self.selection
        ]))


__all__ = [
    'Tuple',
    'Iterable',
    'Strategy',
    'Individual',
    'Population'
]
