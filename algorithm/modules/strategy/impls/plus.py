from ..strategy import *


class Plus(Strategy):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        Strategy.__init__(self, self.mu, **kwargs)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        size = max(self.mu, self.lmbda)
        parents = [next(generator) for _ in range(size)]
        children = map(self.mutation.mutate, parents[:self.lmbda])

        return parents[:self.mu], list(children)

    def __len__(self):
        return self.mu + self.lmbda

    def __str__(self):
        return 'Strategy: (%d + %d)' % (self.mu, self.lmbda)


__all__ = ['Plus']
