from ..function import *
from ...concurrency import Task

from copy import copy
from time import time as now


class GuessAndDetermine(Function):
    type = 'gad'
    name = 'Function: Guess-and-Determine'

    def __get_next_values(self, values):
        new_values, i = copy(values), len(values) - 1
        while i >= 0 and new_values[i] != 0:
            new_values[i] = 0
            i -= 1

        if i < 0:
            return None
        else:
            new_values[i] = 1
            return new_values

    def __main_phase(self, backdoor, result, count, **kwargs):
        concurrency, rs = kwargs['concurrency'], kwargs['rs']
        output, instance = kwargs['output'], kwargs['instance']
        output.debug(1, 0, 'Generating main cases...')

        tasks = []
        for i in range(count):
            tasks.append(Task(i, backdoor=backdoor.values(rs=rs), **instance.values(result.solution)))

        output.debug(1, 0, 'Solving...')
        timestamp = now()
        results = concurrency.solve(tasks, **kwargs)
        time = now() - timestamp

        output.debug(1, 0, 'Has been solved %d cases by %.2f seconds' % (len(results), time))
        if len(results) != count:
            output.debug(0, 0, 'Warning! len(results) != count')

        return results

    def __solve(self, chunk, **kwargs):
        concurrency, output = kwargs['concurrency'], kwargs['output']
        output.debug(1, 0, 'Solve chunk with size: %d' % len(chunk))

        timestamp = now()
        results = concurrency.solve(chunk, **kwargs)
        time = now() - timestamp

        output.debug(1, 0, 'Has been solved %d tasks by %.2f seconds' % (len(results), time))
        if len(chunk) != len(results):
            output.debug(0, 0, 'Warning! len(chunk) != len(results)')

        return results

    def evaluate(self, backdoor: Backdoor, cases: List[Result], count: int, **kwargs) -> List[Result]:
        concurrency, rs = kwargs['concurrency'], kwargs['rs']
        output, instance = kwargs['output'], kwargs['instance']
        output.debug(1, 0, 'Compute for backdoor: %s' % backdoor)

        # init
        output.st_timer('Evaluate_init', 'init_solve')
        if instance.has_values():
            timestamp = now()
            task = Task(0, proof=True, secret_key=instance.secret_key.values(rs=rs))
            result = concurrency.single(task, **kwargs)
            output.debug(1, 0, 'Init case solved by %.2f seconds' % (now() - timestamp))
        else:
            result = Result(0, True, 0, {}, [])
            output.debug(1, 0, 'Skip init phase')
        output.ed_timer('Evaluate_init')

        output.st_timer('Evaluate_main', 'main_solve')
        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            solved = self.__main_phase(backdoor, result, case_count, **kwargs)
            cases.extend(solved)
        output.ed_timer('Evaluate_main')

        return cases

    def verify(self, backdoor: Backdoor, count: int, st: int, **kwargs) -> List[Result]:
        concurrency, rs = kwargs['concurrency'], kwargs['rs']
        output, instance = kwargs['output'], kwargs['instance']
        output.debug(1, 0, 'Compute for backdoor: %s' % backdoor)

        output.st_timer('Evaluate_init', 'init_solve')
        if instance.has_values():
            timestamp = now()
            task = Task(0, proof=True, secret_key=instance.secret_key.values(rs=rs))
            result = concurrency.single(task, **kwargs)
            output.debug(1, 0, 'Init case solved by %.2f seconds' % (now() - timestamp))
        else:
            result = Result(0, True, 0, {}, [])
            output.debug(1, 0, 'Skip init phase')
        output.ed_timer('Evaluate_init')

        variables = backdoor.snapshot()
        values = [1 if st & (1 << i) else 0 for i in range(len(backdoor))][::-1]

        cases, chunk = [], []
        for i in range(st, st + count):
            assumption = [x if values[j] else -x for j, x in enumerate(variables)]
            chunk.append(Task(i, bd=assumption, **instance.values(solution=result.solution)))
            values = self.__get_next_values(values)

            if len(chunk) >= self.chunk_size:
                results = self.__solve(chunk, **kwargs)
                cases.extend(results)
                chunk = []

        if len(chunk) > 0:
            results = self.__solve(chunk, **kwargs)
            cases.extend(results)

        return cases

    def calculate(self, backdoor: Backdoor, cases: List[Result], **kwargs) -> Info:
        output = kwargs['output']
        # output.debug(1, 0, 'Counting statistic...')

        ballast = 2 ** len(backdoor)
        time_sum, value_sum = 0, 0
        statistic = {'IND': 0, 'DET': 0}
        output.st_timer('Calculate_cycle', 'cycle')
        for case in cases:
            time_sum += case.time
            value_sum += case.value
            statistic['IND' if case.status is None else 'DET'] += 1
        output.debug(1, 0, 'Statistic: %s' % statistic)
        output.ed_timer('Calculate_cycle')

        output.st_timer('Calculate_mul', 'mul')
        ev, et = float(value_sum) / len(cases), time_sum / len(cases)
        # output.debug(1, 0, 'Averaged measure: %.7g for %d cases' % (ev, len(cases)))

        value, t_value = ballast * ev, ballast * et
        # output.debug(1, 0, 'Estimation: %.7g (%.7g)' % (value, t_value))
        output.ed_timer('Calculate_mul')
        return Info(value, statistic)


__all__ = [
    'GuessAndDetermine'
]
