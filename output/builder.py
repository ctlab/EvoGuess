from output.cell import OutputCell


class CellBuilder:
    def __init__(self, keygen):
        self.kwargs = {'keygen': keygen}

    def build(self):
        self.kwargs.get('base') or self.base()
        return OutputCell(**self.kwargs)

    def base(self, path='output/_log'):
        self.kwargs['base'] = path
        return self

    def conference(self, name=''):
        self.kwargs['conference'] = name
        return self

    def logger(self, name='log'):
        self.kwargs['log'] = name
        return self

    def debugger(self, verb=0, name='debug', size=1):
        gp = lambda rank: '_'.join([name, str(rank)])
        self.kwargs['debug'] = verb, map(gp, range(size))
        return self

    def description(self, text=''):
        self.kwargs['description'] = text
        return self
