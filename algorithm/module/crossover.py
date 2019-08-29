from numpy.random import randint, rand


class Crossover:
    name = 'crossover'

    def __init__(self, **kwargs):
        pass

    def cross(self, b1, b2):
        raise NotImplementedError

    def __str__(self):
        return self.name


class OnePointCrossover(Crossover):
    def cross(self, b1, b2):
        new_v = b1.get_mask()
        new_w = b2.get_mask()

        pos = randint(len(new_v))

        for i in range(pos, len(new_v)):
            new_v[i], new_w[i] = new_w[i], new_v[i]

        return b1.get_copy(new_v), b2.get_copy(new_w)

    def __str__(self):
        return 'crossover: one-point'


class TwoPointCrossover(Crossover):
    def cross(self, b1, b2):
        new_v = b1.get_mask()
        new_w = b2.get_mask()

        a = randint(len(new_v))
        b = randint(len(new_v))

        if a > b:
            a, b = b, a

        for i in range(a, b):
            new_v[i], new_w[i] = new_w[i], new_v[i]

        return b1.get_copy(new_v), b2.get_copy(new_w)

    def __str__(self):
        return 'crossover: two-point'


class UniformCrossover(Crossover):
    def __init__(self, **kwargs):
        Crossover.__init__(self, **kwargs)
        self.p = float(kwargs['p'])

    def cross(self, b1, b2):
        new_v = b1.get_mask()
        new_w = b2.get_mask()
        distribution = rand(len(new_v))

        for i in range(len(new_v)):
            if self.p >= distribution[i]:
                new_v[i], new_w[i] = new_w[i], new_v[i]

        return b1.get_copy(new_v), b2.get_copy(new_w)

    def __str__(self):
        return 'crossover: uniform (%f)' % self.p


crossovers = {
    'one-point': OnePointCrossover,
    'two-point': TwoPointCrossover,
    'uniform': UniformCrossover
}
