from .case import Case
from typing import List

Iteration = List[Case]


class Parser:
    def parse_file(self, path: str) -> List[Iteration]:
        return self.parse(self.__read(path))

    def parse(self, data: str) -> List[Iteration]:
        raise NotImplementedError

    @staticmethod
    def __read(path: str) -> str:
        with open(path) as f:
            lines = f.readlines()
            return [x[:-1] for x in lines]


__all__ = [
    'Case',
    'List',
    'Parser',
    'Iteration'
]
