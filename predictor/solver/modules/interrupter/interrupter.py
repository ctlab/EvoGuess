from ...tools import *

from typing import List


class Interrupter:
    def __init__(self, **kwargs):
        self.tl = kwargs['tl']

    def hang(self, args: ArgsBuilder) -> ArgsBuilder:
        raise NotImplementedError


__all__ = [
    'List',
    'ArgsBuilder',
    'Interrupter'
]
