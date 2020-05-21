from ..mutation import *


class Configurator(Mutation):
    name = 'Mutation: Configurator'

    def __init__(self, *options, **kwargs):
        self.options = options
        self.function = options[0]['f']
        super().__init__(**kwargs)

    def mutate(self, i: Individual) -> Individual:
        return self.function.mutate(i)

    def configure(self, limits):
        for option in self.options:
            if option['?'](limits):
                self.function = option['f']
                print(limits, self.function)
                return self.function

        print(limits, self.function)
        return self.function

    def __str__(self):
        return '\n'.join(map(str, [
            self.name + (' (seed: %s)' % self.seed if self.seed else ''),
            *('  ' + str(option['f']) for option in self.options)
        ]))


__all__ = [
    'Configurator'
]
