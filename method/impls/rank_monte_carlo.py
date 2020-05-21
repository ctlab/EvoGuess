from ..method import *

from pickle import dumps, loads


class RankMonteCarlo(Method):
    name = 'Method: Rank MonteCarlo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function = kwargs['function']

    def run(self, backdoor: Backdoor, **kwargs) -> Estimation:
        count = kwargs.pop('count')
        cases = self.function.evaluate(backdoor, [], count, **self.kwargs, **kwargs)
        cases.insert(0, self.rank)

        if self.size > 1:
            self.output.debug(2, 1, 'Gathering cases from %d nodes...' % self.size)
            g_cases = self.comm.gather(dumps(cases), root=0)

            if self.rank == 0:
                self.output.debug(2, 1, 'Been gathered cases from %d nodes' % self.size)
                cases = [loads(g_case) for g_case in g_cases]
        else:
            cases = [cases]

        return Estimation(cases, 0.)

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.function,
        ]))


__all__ = [
    'RankMonteCarlo'
]
