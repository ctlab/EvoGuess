from numpy.random import rand


class PopulationRoulette:
    def __init__(self, sorted_P_v):
        self.Q_roulette = []
        length = len(sorted_P_v)
        s = 0.
        for i in range(length):
            v = 0.
            for j in range(length):
                v += sorted_P_v[i][1] / sorted_P_v[j][1]
            s = s + (1. / v) if (i + 1 < length) else 1.
            self.Q_roulette.append((sorted_P_v[i][0], s))

    def get_individual(self, p):
        for q in self.Q_roulette:
            if q[1] >= p:
                return q[0]


class EvolutionStrategy:
    name = 'strategy'
    
    def __init__(self, alive_count):
        self.alive_count = alive_count

    def get_P_size(self):
        raise NotImplementedError

    def get_next_P(self, mc_f, sorted_P_v):
        raise NotImplementedError

    def get_Q(self, sorted_P_v):
        Q = []
        for i in range(self.alive_count):
            Q.append(sorted_P_v[i][0])

        return Q
    
    def __str__(self):
        return self.name


class MuCommaLambda(EvolutionStrategy):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        EvolutionStrategy.__init__(self, 0)

    def get_P_size(self):
        return self.lmbda

    def get_next_P(self, mc_f, sorted_P_v):
        mutation_f = mc_f[0]
        P = []
        roulette = PopulationRoulette(sorted_P_v)
        distribution = rand(self.lmbda)
        for i in range(self.lmbda):
            q = roulette.get_individual(distribution[i])
            new_p = mutation_f(q)
            P.append(new_p)

        return P

    def __str__(self):
        return 'Strategy (%d, %d)' % (self.mu, self.lmbda)


class MuPlusLambda(MuCommaLambda):
    def __init__(self, **kwargs):
        self.mu = kwargs['mu']
        self.lmbda = kwargs['lmbda']
        EvolutionStrategy.__init__(self, self.mu)

    def get_P_size(self):
        return self.mu + self.lmbda

    def get_next_P(self, mc_f, sorted_P_v):
        P = self.get_Q(sorted_P_v)
        P.extend(MuCommaLambda.get_next_P(self, mc_f, sorted_P_v))

        return P

    def __str__(self):
        return 'strategy: (%d + %d)' % (self.mu, self.lmbda)


class Genetic(EvolutionStrategy):
    def __init__(self, **kwargs):
        self.m = kwargs['m']
        self.l = kwargs['l']
        self.c = kwargs['c']
        EvolutionStrategy.__init__(self, self.l)

    def get_P_size(self):
        return self.m + self.l + self.c

    def get_next_P(self, mc_f, sorted_P_v):
        mutation_f = mc_f[0]
        crossover_f = mc_f[1]
        P = self.get_Q(sorted_P_v)

        roulette = PopulationRoulette(sorted_P_v)
        distribution = rand(self.m)
        for i in range(self.m):
            q = roulette.get_individual(distribution[i])
            new_p = mutation_f(q)
            P.append(new_p)

        distribution = rand(self.c * 3)
        for i in range(self.c):
            v = roulette.get_individual(distribution[i])
            w = roulette.get_individual(distribution[self.c + i])

            new_v, new_w = crossover_f(v, w)
            P.append(new_v if distribution[2 * self.c + i] < 0.5 else new_w)

        return P

    def __str__(self):
        return 'genetic: (%d, %d, %d)' % (self.m, self.l, self.c)


strategies = {
    'comma': MuCommaLambda,
    'plus': MuPlusLambda,
    'genetic': Genetic
}