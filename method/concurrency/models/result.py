from os import getpid
from typing import List, Optional

statuses = {
    True: 'SAT',
    None: 'IND',
    False: 'UNSAT'
}


class Result:
    def __init__(self, i: int, status: Optional[bool], time: int, solution: Optional[List[int]]):
        self.i = i
        self.time = time
        self.pid = getpid()
        self.status = status
        self.solution = solution

    def __str__(self):
        return '%s(%f) at %s' % (statuses[self.status], self.time, self.pid)


__all__ = [
    'Result'
]
