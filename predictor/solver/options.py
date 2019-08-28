class SolverOptions:
    def __init__(self, **kwargs):
        self.options = {}
        self.update(**kwargs)

    def update(self, **kwargs):
        for key in kwargs.keys():
            self.options[key] = kwargs[key]

    def get(self):
        return map(lambda x: '%s=%s' % (x[0], x[1]), self.options.items())

    def __len__(self):
        return len(self.options)

    def __str__(self):
        return ' '.join(self.get())
