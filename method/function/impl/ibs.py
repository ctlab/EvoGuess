from ..function import *

from os import getpid


def ibs_task(i, solver, instance, data, limit):
    return i, getpid(), None, {}


class InverseBackdoorSets(Function):
    def __init__(self, limit, *args, **kwargs):
        self.limit = limit
        super().__init__(*args, **kwargs)

    type = 'gad'
    name = 'Function: Guess-and-Determine'

    def get_tasks(self, backdoor: Backdoor, *dimension) -> Iterable[Task]:
        return []

    def calculate(self, backdoor: Backdoor, *cases: Case) -> Result:
        return 0., 0., {}


__all__ = [
    'InverseBackdoorSets'
]
