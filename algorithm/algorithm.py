from .models import *

from typing import List
from predictor.instance.models.var import Backdoor


class Algorithm:
    name = 'Algorithm'

    def __init__(self, **kwargs):
        self.values = {}
        self.limit = kwargs['limit']
        self.output = kwargs['output']
        self.sampling = kwargs['sampling']
        self.predictor = kwargs["predictor"]

    def start(self, backdoor: Backdoor) -> List[Individual]:
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.sampling,
            self.predictor
        ]))

    def log_info(self):
        self.output.log('\n'.join('-- ' + s for s in str(self).split('\n')))
        return self

    def log_delim(self):
        self.output.log('------------------------------------------------------')
        return self

    def log_it_header(self, it, more=''):
        self.output.log('Iteration: %d%s' % (it, ' (%s)' % more if len(more) else ''))
        return self

    def log_run(self, backdoor, count):
        self.output.log('Run predictor on backdoor: %s' % backdoor,
                        'With %d cases:' % count)
        return self

    def log_end(self, value):
        self.output.log('End prediction with value: %.7g' % value)
        return self

    def log_hashed(self, backdoor, value):
        self.output.log('Hashed backdoor: %s' % backdoor,
                        'With value: %.7g\n' % value)
        return self


__all__ = [
    'List',
    'Backdoor',
    'Algorithm',
    'Individual'
]
