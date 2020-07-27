from .result import Result


class Task:
    def __init__(self, i, proof=False, tl=0, **assumptions):
        self.i = i
        self.tl = tl
        self.proof = proof
        self.assumptions = assumptions

    def get(self, in_bits=True, out_bits=True):
        assumptions = []

        if in_bits and out_bits:
            for values in self.assumptions.values():
                assumptions.extend(values)

            return assumptions

        if in_bits:
            for key, values in self.assumptions.items():
                if key in ['secret_key', 'backdoor']:
                    assumptions.extend(values)
        if out_bits:
            for key, values in self.assumptions.items():
                if key in ['key_stream', 'public_key']:
                    assumptions.extend(values)

        return assumptions

    def resolve(self, status, time, stats, solution=None):
        return Result(self.i, status, time, stats, solution if self.proof else None)

    def __copy__(self):
        return Task(self.i, proof=self.proof, tl=self.tl, **self.assumptions)


__all__ = [
    'Task'
]
