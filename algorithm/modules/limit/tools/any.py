from ..limit import *


class Any(Limit):
    name = 'Limit: Any'

    def __init__(self, *args):
        super().__init__()
        self.args = args
        for arg in args:
            arg.limits = self.limits

    def exhausted(self) -> bool:
        print([arg.exhausted() for arg in self.args])
        return any(arg.exhausted() for arg in self.args)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            *self.args
        ]))


__all__ = [
    'Any'
]
