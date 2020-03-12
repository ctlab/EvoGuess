from ..models import *
from typing import List, Iterable

from numpy import concatenate


class ArgsBuilder:
    def __init__(self, solver):
        self.tl = 0
        self.wrappers = []
        # self.options = set()
        self.solver = solver

    def wrap(self, args: List[str]):
        self.wrappers.append(args)
        return self

    def limit(self, time: int):
        self.tl = time
        return self

    # def tune(self, options: Iterable[SolverOption]):
    #     map(self.options.add, options)
    #     return self

    def build(self) -> List[str]:
        args = list(concatenate(self.wrappers[::-1] or [[]]))
        args.extend(self.solver.get_args(self.tl))
        # args.extend(map(str, self.options))

        return args


__all__ = [
    'ArgsBuilder'
]
