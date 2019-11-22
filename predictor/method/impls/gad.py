from ..method import *
from ...concurrency.models import Task

from time import time as now


class GuessAndDetermine(Method):
    type = 'gad'

    def __main_phase(self, backdoor, solution, count, **kwargs):
        output = kwargs['output']
        rs, cipher = kwargs['rs'], kwargs['instance']
        output.debug(1, 0, 'Generating main cases...')

        tasks = []
        for i in range(count):
            tasks.append(Task(i, bd=backdoor.values(rs=rs), **cipher.values(solution)))

        output.debug(1, 0, 'Solving...')
        timestamp = now()
        results = self.concurrency.solve(tasks, **kwargs)
        time = now() - timestamp

        output.debug(1, 0, 'Has been solved %d cases by %.2f seconds' % (len(results), time))
        if len(results) != count:
            output.debug(0, 0, 'Warning! len(results) != count')

        return results

    def compute(self, backdoor: Backdoor, cases: List[Result], count: int, **kwargs) -> List[Result]:
        output = kwargs['output']
        rs, cipher = kwargs['rs'], kwargs['instance']
        output.debug(1, 0, 'Compute for backdoor: %s' % backdoor)

        # init
        task = Task(0, sk=cipher.secret_key.values(rs=rs))
        result = self.concurrency.single(task, **kwargs)

        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            solved = self.__main_phase(backdoor, result.solution, case_count, **kwargs)
            cases.extend(solved)

        return cases

    def estimate(self, backdoor: Backdoor, cases: List[Result], **kwargs) -> Estimation:
        output, cipher = kwargs['output'], kwargs['instance']
        output.debug(1, 0, 'Counting statistic...')

        statistic = self._count(cases)
        output.debug(1, 0, 'Statistic: %s' % statistic)

        time_sum = sum(case.time for case in cases)
        output.debug(1, 0, 'Calculating value...',
                     'Averaged time: %f for %d cases' % (time_sum / len(cases), len(cases)))
        value = (2 ** len(backdoor)) * time_sum / len(cases)
        output.debug(1, 0, 'Estimation: %.7g' % value)

        return Estimation(value, statistic)


__all__ = [
    'GuessAndDetermine'
]
