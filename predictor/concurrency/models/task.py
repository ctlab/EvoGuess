from .result import Result


class Task:
    def __init__(self, i, tl=0, **assumptions):
        self.i = i
        self.tl = tl
        self.assumptions = assumptions

    def get(self):
        assumptions = []
        for values in self.assumptions.values():
            assumptions.extend(values)

        return assumptions

    def resolve(self, status, time, solution=None):
        return Result(self.i, status, time, solution)


__all__ = [
    'Task'
]
