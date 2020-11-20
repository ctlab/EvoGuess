from ..function import *

from os import getpid
from time import time as now


def bits_to_values(bits, variables):
    assert len(bits) >= len(variables)
    return [x if bits[i] else -x for i, x in enumerate(variables)]


def gad_task(i, solver, instance, data):
    st_timestamp = now()
    bits = decode_bits(data)
    bd_vars = instance.secret_key.filter(bits[0])
    assumptions = bits_to_values(bits[1], bd_vars)
    for i, interval in enumerate(instance.intervals()):
        # todo: inspect function
        assumptions.extend(interval.values(bits[i + 2]))

    status, stats, _, _ = solver.solve(instance.clauses(), assumptions)
    result = (i, getpid(), status, stats, (st_timestamp, now()))
    return encode_result(result)


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
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0
        for case in cases:
            statistic[case[2]] += 1
            time_sum += case[3]['time']
            value_sum += self.measure.get(case[3])
            process_time += case[4][1] - case[4][0]

        time, value, = None, None
        count = 2 ** len(backdoor)
        if count == len(cases):
            time, value = time_sum, value_sum
        elif len(cases) > 0:
            time = float(time_sum) / len(cases) * count
            value = float(value_sum) / len(cases) * count

        return statistic, {
            'time': time,
            'value': value,
            'count': len(cases),
            'job_time': time_sum,
            'process_time': process_time
        }


__all__ = [
    'GuessAndDetermine'
]
