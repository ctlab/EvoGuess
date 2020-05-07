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

    def get_status(self):
        return statuses[self.status]

    def __str__(self):
        return '%s(%f) at %s' % (statuses[self.status], self.time, self.pid)

    def __copy__(self):
        result = Result(self.i, self.status, self.time, self.solution)
        result.pid = self.pid
        return result


__all__ = [
    'Result'
]
