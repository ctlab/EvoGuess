from typing import Tuple, Dict, Iterable

from ..solver.types import Solver
from structure.array import Backdoor
from concurrency.concurrency import Task

Case = Tuple[int, int, bool, Dict[str, int]]
Result = Tuple[Dict[bool, int], Dict[str, int]]


def encode_bits(bits):
    return bits


def decode_bits(data):
    return data


class Function:
    type = None
    name = 'Function'

    def __init__(self, solver: Solver, instance, measure):
        self.solver = solver
        self.instance = instance
        self.measure = measure

    def get_tasks(self, backdoor: Backdoor, *dimension, **kwargs) -> Iterable[Task]:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, *cases: Case) -> Result:
        raise NotImplementedError

    def get_values(self, *cases: Case) -> Iterable[float]:
        return [self.measure.get(case[3]) for case in cases]

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.solver,
            self.measure,
        ]))


__all__ = [
    'Task',
    'Case',
    'Result',
    'Solver',
    'Iterable',
    'Backdoor',
    'Function',
    'encode_bits',
    'decode_bits'
]
