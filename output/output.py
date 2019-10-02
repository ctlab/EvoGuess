from typing import Iterable
from os.path import join


class Output:
    def __init__(self, **kwargs):
        self.path = kwargs['path']
        if isinstance(self.path, list):
            self.path = join(*self.path)

    def log(self, *strs: Iterable[str]) -> None:
        raise NotImplementedError

    def debug(self, verb: int, level: int, *strs: Iterable[str]) -> None:
        raise NotImplementedError


__all__ = [
    'Output',
    'Iterable'
]
