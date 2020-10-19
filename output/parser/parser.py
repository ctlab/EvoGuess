from typing import List, Tuple

from structure.array import Backdoor

Estimation = Tuple[Backdoor, float]
Iteration = List[Estimation]


class Parser:
    def parse_file(self, path: str) -> List[Iteration]:
        return self.parse(self._read(path))

    def parse(self, data: str) -> List[Iteration]:
        raise NotImplementedError

    @staticmethod
    def _read(path: str) -> str:
        with open(path) as f:
            lines = f.readlines()
            return [x[:-1] for x in lines]


__all__ = [
    'Parser',
    'Iteration'
]
