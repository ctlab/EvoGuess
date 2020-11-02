from typing import Tuple, Dict, Iterable

from ..solver.types import Solver
from structure.array import Backdoor
from concurrency.concurrency import Task

Case = Tuple[int, int, bool, Dict[str, int]]
Result = Tuple[Dict[bool, int], Dict[str, int]]

BASIS = 8


def to_bits(number):
    assert number < 1 << BASIS
    return [1 if number & (1 << (BASIS - i - 1)) else 0 for i in range(BASIS)]


def to_number(bits):
    assert len(bits) <= BASIS
    return sum([1 << (BASIS - i - 1) for i, bit in enumerate(bits) if bit])


def encode_bits(bits):
    data = []
    for array in bits:
        numbers = []
        for i in range(0, len(array), BASIS):
            numbers.append(to_number(array[i:i + BASIS]))
        data.append(numbers)
    # print([[1 if bit else 0 for bit in array] for array in bits])
    # print(decode_bits(data))
    # print('--')
    return data


def decode_bits(data):
    bits = []
    for numbers in data:
        array = []
        for number in numbers:
            array.extend(to_bits(number))
        bits.append(array)
    return bits


class Function:
    type = None
    name = 'Function'

    def __init__(self, solver: Solver, instance, measure, *args, **kwargs):
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
