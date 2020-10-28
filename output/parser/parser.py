from typing import List, Tuple

from os import listdir
from os.path import join
from structure.individual import Individual

Iteration = List[Individual]


class Parser:
    def parse(self, path: str) -> List[Iteration]:
        files = listdir(path)
        log_files = [file for file in files if 'log' in file]
        print('Found %d log files' % len(log_files))

        iterations = []
        for log_file in sorted(log_files):
            log_path = join(path, log_file)
            data = self._read(log_path)
            iterations.extend(self.parse_data(data))
        return iterations

    def parse_data(self, data: str) -> List[Iteration]:
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
