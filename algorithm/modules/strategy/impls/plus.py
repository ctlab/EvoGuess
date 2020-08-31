from ..strategy import *


class Plus(Strategy):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        super().__init__(self.mu, **kwargs)
        self.name = 'Strategy: (%d + %d)' % (self.mu, self.lmbda)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        # size = max(self.mu, self.lmbda)
        # parents = [next(generator) for _ in range(size)]
        # children = map(self.mutation.mutate, parents[:self.lmbda])
        # return parents[:self.mu], list(children)

        parents = [next(generator) for _ in range(self.lmbda)]
        return [], list(map(self.mutation.mutate, parents))

    def __len__(self):
        return self.mu + self.lmbda


__all__ = ['Plus']
