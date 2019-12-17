from ..method import *
from ...concurrency.models import Task

from time import time as now


class InverseBackdoorSets(Method):
    type = 'ibs'
    name = 'Method: Inverse Backdoor Sets'

    def __init__(self, **kwargs):
        Method.__init__(self, **kwargs)
        self.tl = kwargs['time_limit']
        self.corrector = kwargs.get('corrector')

    def __init_phase(self, count, **kwargs):
        output = kwargs['output']
        rs, instance = kwargs['rs'], kwargs['instance']
        output.debug(1, 0, 'Generating init cases...')

        if instance.has_values():
            tasks = [Task(i, sk=instance.secret_key.values(rs=rs)) for i in range(count)]

            timestamp = now()
            results = self.concurrency.propagate(tasks, **kwargs)
            time = now() - timestamp

            output.debug(1, 0, 'Has been solved %d init cases by %.2f seconds' % (len(results), time))
            if count != len(results):
                output.debug(0, 0, 'Warning! count != len(results)')
        else:
            results = [Result(i, True, 0, []) for i in range(count)]
            output.debug(1, 0, 'Skip init phase')

        return results

    def __main_phase(self, backdoor, inited, **kwargs):
        output = kwargs['output']
        rs, cipher = kwargs['rs'], kwargs['instance']
        output.debug(1, 0, 'Generating main cases...')

        tasks = []
        for result in inited:
            tasks.append(Task(result.i, tl=self.tl, bd=backdoor.values(solution=result.solution),
                              **cipher.values(result.solution)))

        output.debug(1, 0, 'Solving...')
        timestamp = now()
        results = self.concurrency.solve(tasks, **kwargs)
        time = now() - timestamp

        output.debug(1, 0, 'Has been solved %d cases by %.2f seconds' % (len(results), time))
        if len(inited) != len(results):
            output.debug(0, 0, 'Warning! len(inited) != len(results)')

        return results

    def compute(self, backdoor: Backdoor, cases: List[Result], count: int, **kwargs) -> List[Result]:
        output = kwargs['output']
        output.debug(1, 0, 'Compute for backdoor: %s' % backdoor)
        output.debug(1, 0, 'Use time limit: %s' % self.tl)

        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            inited = self.__init_phase(case_count, **kwargs)
            solved = self.__main_phase(backdoor, inited, **kwargs)
            cases.extend(solved)

        return cases

    def estimate(self, backdoor: Backdoor, cases: List[Result], **kwargs) -> Estimation:
        output, cipher = kwargs['output'], kwargs['instance']
        output.debug(1, 0, 'Counting statistic...')

        statistic, strs, tl = self._count(cases), [], self.tl
        output.debug(1, 0, 'Statistic: %s' % statistic)
        if self.corrector is not None:
            output.debug(1, 0, 'Correcting time limit...')
            tl, dis = self.corrector.correct(cases, tl)
            output.debug(1, 0, "Corrected time limit: %.6f" % tl)
            statistic['DIS'] = dis
            statistic['DET'] -= dis
            output.debug(1, 0, "New statistic: %s" % statistic)
            strs.append('New time limit: %.6f' % tl)

        output.debug(1, 0, 'Calculating value...')
        xi = float(statistic['DET']) / float(len(cases))
        if xi != 0:
            value = (2 ** len(backdoor)) * tl * (3 / xi)
        else:
            value = (2 ** len(cipher.secret_key)) * tl
        output.debug(1, 0, 'Estimation: %.7g' % value)

        return Estimation(value, statistic, *strs)


__all__ = [
    'InverseBackdoorSets'
]
