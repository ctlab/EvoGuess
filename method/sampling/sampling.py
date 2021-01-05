from typing import Tuple
from structure.array import Backdoor


class Sampling:
    name = 'Sampling'

    def __init__(self, instance):
        self.base = instance.base

    def get_count(self, backdoor: Backdoor, values=()):
        raise NotImplementedError

    def get_max(self) -> Tuple[int, int]:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Tuple',
    'Backdoor',
    'Sampling'
]
