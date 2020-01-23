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
        self.save_init = kwargs.get('save_init', True)
        self.reset_init = kwargs.get('reset_init', 10)

        self.saved = {}
        self.init_timer = 0

    def __init_phase(self, rng, **kwargs):
        output = kwargs['output']
        rs, instance = kwargs['rs'], kwargs['instance']
        output.debug(1, 0, 'Generating init cases...')

        results = [None] * len(rng)
        if self.save_init:
            task_rng = []
            for i, j in enumerate(rng):
                if j in self.saved:
                    results[i] = self.saved[j]
                else:
                    task_rng.append((i, j))
        else:
            task_rng = enumerate(rng)

        output.debug(1, 1, 'Use %d saved cases of %d' % (len(rng) - len(task_rng), len(rng)))
        while len(task_rng) > 0:
            if instance.has_values():
                tasks = [Task(i, sk=instance.secret_key.values(rs=rs)) for i in task_rng]

                timestamp = now()
                c_results = self.concurrency.propagate(tasks, **kwargs)
                time = now() - timestamp

                output.debug(1, 1, 'Has been solved %d init cases by %.2f seconds' % (len(c_results), time))
                for result in c_results:
                    try:
                        i, j = result.i
                        task_rng.remove((i, j))
                        results[i] = result
                    except ValueError:
                        output.debug(0, 1, 'Ranged value not in task_rng!')

                if len(task_rng) > 0:
                    output.debug(0, 1, 'Warning! len(task_rng) > 0')
            else:
                for i, j in task_rng:
                    results[i] = Result((i, j), True, 0, [])
                output.debug(1, 1, 'Skip init phase')
                task_rng.clear()

        if self.save_init:
            for i, j in enumerate(rng):
                if j not in self.saved:
                    self.saved[j] = results[i]

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

        self.init_timer += 1
        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            rng = range(len(cases), len(cases) + case_count)  # todo: допилить
            inited = self.__init_phase(rng, **kwargs)
            solved = self.__main_phase(backdoor, inited, **kwargs)
            cases.extend(solved)

        if self.init_timer == self.reset_init:
            self.saved = {}
            self.init_timer = 0

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
