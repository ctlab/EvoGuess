from .result import Result


class Task:
    def __init__(self, i, proof=False, tl=0, **assumptions):
        self.i = i
        self.tl = tl
        self.proof = proof
        self.assumptions = assumptions

    def get(self):
        assumptions = []
        for values in self.assumptions.values():
            assumptions.extend(values)

        return assumptions

    def resolve(self, status, time, solution=None):
        return Result(self.i, status, time, solution if self.proof else None)

    def __copy__(self):
        return Task(self.i, proof=self.proof, tl=self.tl, **self.assumptions)


__all__ = [
    'Task'
]
