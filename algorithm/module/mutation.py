from numpy.random import rand


class Mutation:
    name = 'mutation'

    def __init__(self, **kwargs):
        pass

    def mutate(self, backdoor):
        raise NotImplementedError

    def __str__(self):
        return self.name


class UniformMutation(Mutation):
    def __init__(self, **kwargs):
        Mutation.__init__(self, **kwargs)
        self.scale = float(kwargs['scale'])

    def mutate(self, backdoor):
        new_v = backdoor.get_mask()
        p = self.scale / len(new_v)
        flag = True
        while flag:
            distribution = rand(len(new_v))

            for d in distribution:
                if p >= d:
                    flag = False

        for i in range(len(new_v)):
            if p >= distribution[i]:
                new_v[i] = not new_v[i]

        return backdoor.get_copy(new_v)

    def __str__(self):
        return 'mutation: uniform (%.1f)' % self.scale


mutations = {
    'uniform': UniformMutation,
}