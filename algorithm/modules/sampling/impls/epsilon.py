from ..sampling import *


class Epsilon(Sampling):
    def __init__(self, mn, mx, step, eps):
        self.min, self.max = mn, mx
        self.step, self.eps = step, eps
        self.name = 'Sampling: Epsilon (%d..%d)' % (mn, mx)

        self.values, self.keys = {}, []

    def get_size(self, backdoor: Backdoor):
        bd_len = len(backdoor)
        if len(self.keys) == 0:
            return self.min

        if bd_len in self.values:
            return self.values[bd_len]

        i, key = 1, self.keys[0]
        value = self.values[key]
        while i < len(self.keys) and bd_len > key:
            key, i = self.keys[i], i + 1
            value = self.values[key]

        return value

    def analyse(self, population):
        for individual in population:
            backdoor = individual.backdoor

            bd_len = len(backdoor)
            if bd_len not in self.values:
                if len(self.keys) == 0:
                    self.keys.append(bd_len)
                    self.values[bd_len] = self.min
                else:
                    i, key = 1, self.keys[0]
                    value = self.values[key]
                    while i < len(self.keys) and bd_len > key:
                        key, i = self.keys[i], i + 1
                        value = self.values[key]

                    self.values[bd_len] = value
                    self.keys.insert(i if bd_len > key else i - 1, bd_len)

            value = self.values[bd_len]
            if individual.eps > self.eps:
                self.values[bd_len] = min(self.max, value + self.step)
            else:
                self.values[bd_len] = max(self.min, value - self.step)

        print(self.keys)
        print(self.values)
        print('-' * 15)


__all__ = [
    'Epsilon'
]
