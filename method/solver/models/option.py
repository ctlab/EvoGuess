class SolverOption:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def str(self, form):
        return form % (self.name, self.value)

    def __str__(self):
        return self.str('%s=%s')

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return self.name == other.name

        return False

    def __hash__(self):
        return hash(self.name)


__all__ = [
    'SolverOption'
]


if __name__ == '__main__':
    a = SolverOption('a', 1)
    b = SolverOption('b', 1)
    c = SolverOption('c', 1)
    s = set([a, b, c])

    a2 = SolverOption('a', 1)
    d = SolverOption('d', 1)
    for o in s:
        print(o)
