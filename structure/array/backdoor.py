import warnings

from copy import copy
from numpy import count_nonzero
from numpy.random.mtrand import RandomState


def get_values(variables, **kwargs):
    if len(variables) == 0: return []
    if 'solution' in kwargs:
        solution = kwargs['solution']
        if len(solution) < variables[-1]:
            raise Exception('Solution has too few variables: %d' % len(solution))

        return [solution[x - 1] for x in variables]
    else:
        random_state = kwargs['rs'] if 'rs' in kwargs else RandomState()
        values = random_state.randint(2, size=len(variables))
        return [x if values[i] else -x for i, x in enumerate(variables)]


class Backdoor:
    # overridden methods
    def __init__(self, _list=()):
        self.list = sorted(set(_list))
        self.length = len(self.list)
        self.mask = [True] * self.length

        if len(self.list) > 0:
            self.min = self.list[0]
            self.max = self.list[-1]

            if len(_list) != self.length:
                warnings.warn('Repeating variables in backdoor', Warning)

            if self.min <= 0:
                raise Exception('Backdoor contains negative numbers or zero')

    def __str__(self):
        if len(self) == 0:
            return '[](0)'

        def itos(il):
            if il[1] - il[0] > 2:
                return '%s..%s' % (il[0], il[1])
            else:
                return ' '.join(map(str, range(il[0], il[1] + 1)))

        variables = self.snapshot()
        s, interval = '[', [variables[0], variables[0]]
        for i in range(1, len(variables)):
            if variables[i] - interval[1] == 1:
                interval[1] = variables[i]
            else:
                s += itos(interval) + ' '
                interval = [variables[i], variables[i]]
        return ''.join([s, itos(interval), '](%d)' % len(variables)])

    def __len__(self):
        return count_nonzero(self.mask)

    def __copy__(self):
        return self.get_copy(self.mask)

    def __iter__(self):
        for i in range(self.length):
            if self.mask[i]:
                yield self.list[i]

    # mask
    def _set_mask(self, mask):
        if len(mask) > self.length:
            self.mask = mask[:self.length]
        else:
            delta = self.length - len(mask)
            self.mask = mask + [False] * delta

    def get_mask(self):
        return copy(self.mask)

    def get_copy(self, mask):
        backdoor = Backdoor(self.list)
        backdoor._set_mask(mask)
        return backdoor

    def reset(self):
        self._set_mask([True] * self.length)

    # main
    def values(self, **kwargs):
        return get_values(self.snapshot(), **kwargs)

    def snapshot(self):
        return [x for (i, x) in enumerate(self.list) if self.mask[i]]

    @staticmethod
    def load(path):
        with open(path) as f:
            lines = [ln.strip() for ln in f.readlines()]
            return [Backdoor.parse(ln) for ln in lines if len(ln) > 0]

    @staticmethod
    def parse(line):
        variables = []
        if len(line) > 0:
            for lit in line.split(' '):
                if '..' in lit:
                    var = lit.split('..')
                    variables.extend(range(int(var[0]), int(var[1]) + 1))
                else:
                    variables.append(int(lit))

        return Backdoor(variables)

    @staticmethod
    def empty():
        return Backdoor()


__all__ = [
    'Backdoor',
    'get_values'
]
