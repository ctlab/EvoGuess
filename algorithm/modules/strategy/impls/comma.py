from ..strategy import *


class Comma(Strategy):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        super().__init__(self.mu, **kwargs)
        self.name = 'Strategy (%d, %d)' % (self.mu, self.lmbda)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        parents = [next(generator) for _ in range(self.lmbda)]
        children = map(self.mutation.mutate, parents)

        return [], list(children)

    def __len__(self):
        return self.lmbda


__all__ = ['Comma']
