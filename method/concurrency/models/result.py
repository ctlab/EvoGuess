from os import getpid
from typing import List, Optional, Dict

statuses = {
    True: 'SAT',
    None: 'IND',
    False: 'UNSAT'
}


class Result:
    def __init__(self, i: int, status: Optional[bool], time: int, stats: Dict[str, int], solution: Optional[List[int]]):
        self.i = i
        self.time = time
        self.value = time
        self.stats = stats
        self.pid = getpid()
        self.status = status
        self.solution = solution

    def get_status(self):
        return statuses[self.status]

    def set_value(self, value):
        self.value = value
        return self

    def __str__(self):
        return '%s(%s) at %s' % (statuses[self.status], self.value, self.pid)

    def __copy__(self):
        result = Result(self.i, self.status, self.time, self.stats, self.solution)
        result.pid = self.pid
        return result.set_value(self.value)


__all__ = [
    'Result'
]
