from structure.array import Backdoor
from ..parser import *

from typing import List
import re


class BaseParser(Parser):
    def __init__(self):
        self.bd_cache = None
        self.bd = re.compile(r'[\[\]]')
        self.ind = re.compile(r'Individuals \((\d+)\):')

    def parse(self, data: str) -> List[Iteration]:
        i, iterations = 0, []
        iteration, i = self._parse_iteration(data, i + 1)

        while iteration is not None:
            iterations.append(iteration)
            try:
                iteration, i = self._parse_iteration(data, i)
            except IndexError as e:
                iteration = None
                print('Parse error (iteration): %s' % e)

        return iterations

    def _parse_iteration(self, data, i):
        if len(data) <= i:
            return None, i

        if data[i].startswith('Iteration'):
            assert data[i + 1].startswith('Individuals')
            ind_count = int(self.ind.findall(data[i + 1])[0])
            i, individuals = i + 2, []
            for j in range(ind_count):
                ind_line = data[i].split(' ')
                _, bd_str, _, value, _, _ = ind_line

                value = float(value)
                backdoor = Backdoor.parse(self.bd.split(bd_str)[1])
                individuals.append((backdoor, value))
                i += 1

            assert data[i].startswith('Time')
            assert data[i + 1].startswith('--')
            return individuals, i + 2
        else:
            return None, i
