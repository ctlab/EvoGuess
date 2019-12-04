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
            data = [str(x).split('\n')[0] for x in lines]

            return data


__all__ = [
    'Case',
    'List',
    'Parser',
    'Iteration'
]
