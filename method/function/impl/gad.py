from ..function import *

from os import getpid


def bits_to_values(bits, variables):
    assert len(bits) == len(variables)
    return [x if bits[i] else -x for i, x in enumerate(variables)]


def gad_task(i, solver, instance, data):
    bits = decode_bits(data)
    bd_vars = instance.secret_key.filter(bits[0])
    assumptions = bits_to_values(bits[1], bd_vars)
    for i, interval in enumerate(instance.intervals()):
        assumptions.extend(interval.values(bits[i + 2]))

    status, stats, _, _ = solver.solve(instance.clauses(), assumptions)
    return i, getpid(), status, stats


class GuessAndDetermine(Function):
    type = 'gad'
    name = 'Function: Guess-and-Determine'

    def get_tasks(self, backdoor: Backdoor, *dimension, **kwargs) -> Iterable[Task]:
        ad_bits = []
        if self.instance.has_intervals():
            clauses = self.instance.clauses()
            assumptions = self.instance.secret_key.values(rs=kwargs['random_state'])
            _, _, solution, _ = self.solver.solve(clauses, assumptions, ignore_key=True)
            for i, interval in enumerate(self.instance.intervals()):
                ad_bits.append(interval.get_bits(solution=solution))

        bd_bits = backdoor.get_mask()
        task_data = [encode_bits([bd_bits, bits, *ad_bits]) for bits in dimension]
        return [(gad_task, i, self.solver, self.instance, data) for i, data in enumerate(task_data)]

    def calculate(self, backdoor: Backdoor, *cases: Case) -> Result:
        time_sum, value_sum = 0, 0
        statistic = {True: 0, False: 0, None: 0}
        for case in cases:
            time_sum += case[3]['time']
            value_sum += self.measure.get(case[3])
            statistic[case[2]] += 1

        count = 2 ** len(backdoor)
        if count == len(cases):
            return value_sum, time_sum, statistic

        time = float(time_sum) / len(cases) * count
        value = float(value_sum) / len(cases) * count
        return value, time, statistic


__all__ = [
    'GuessAndDetermine'
]
