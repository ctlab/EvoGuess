from method.concurrency.models import Result


class Measure:
    name = 'Measure'

    def get(self, result: Result):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Result',
    'Measure'
]
