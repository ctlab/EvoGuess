from ..strategy import *


class Comma(Strategy):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        Strategy.__init__(self, self.mu, **kwargs)

    def tweak(self, generator: Iterable[Individual]) -> Tuple[Population, Population]:
        parents = [next(generator) for _ in range(self.lmbda)]
        print(list(map(str, parents)))
        children = map(self.mutation.mutate, parents)

        return [], list(children)

    def __len__(self):
        return self.lmbda

    def __str__(self):
        return 'Strategy (%d, %d)' % (self.mu, self.lmbda)


__all__ = ['Comma']
