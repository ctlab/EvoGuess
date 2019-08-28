from numpy.random.mtrand import RandomState


def get_values(variables, **kwargs):
    if 'solution' in kwargs:
        solution = kwargs['solution']
        if len(solution) < variables[-1]:
            raise Exception('Solution has too few variables: %d' % len(solution))

        return [x if solution[x - 1] else -x for x in variables]
    else:
        random_state = kwargs['rs'] if 'rs' in kwargs else RandomState()
        values = random_state.randint(2, size=len(variables))
        return [x if values[i] else -x for i, x in enumerate(variables)]


class Interval:
    def __init__(self, st, end):
        self.list = range(st, end)
        self.st, self.end = st, end

        if self.st <= 0:
            raise Exception('Interval contains negative numbers or zero')

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return '%s..%s' % (self.st, self.end - 1)

    def values(self, **kwargs):
        return get_values(self.list, **kwargs)


class KeyStream(Interval):
    def __init__(self, algorithm):
        st = algorithm.key_stream_start
        end = st + algorithm.key_stream_len
        Interval.__init__(self, st, end)


class PublicKey(Interval):
    def __init__(self, algorithm):
        if not hasattr(algorithm, 'public_key_len'):
            raise Exception('%s doesn\'t have a public key' % algorithm.name)

        st = algorithm.public_key_start
        end = st + algorithm.public_key_len
        Interval.__init__(self, st, end)
