from ..parser import *

from typing import List
from structure.array import Backdoor
from structure.individual import Individual

import re


class BaseParser(Parser):
    def __init__(self):
        self.bd_cache = None
        self.popup = re.compile(r'Individuals \((\d+)\):')
        self.ind = re.compile(r'-- \[([\d. ]*)\]\(\d+\) by ([\d.e+]*) \((\d*) samples\)')

    def parse_data(self, data: str) -> List[Iteration]:
        i, iterations = 0, []
        iteration, i = self._parse_iteration(data, i)

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
            ind_count = int(self.popup.findall(data[i + 1])[0])
            i, individuals = i + 2, []
            for j in range(ind_count):
                bd_str, value, samples = self.ind.findall(data[i])[0]

                value = float(value)
                samples = int(samples)
                backdoor = Backdoor.parse(bd_str)
                individual = Individual(backdoor).set(value, count=samples)
                individuals.append(individual)
                i += 1

            assert data[i].startswith('Time')
            assert data[i + 1].startswith('--')
            return individuals, i + 2
        else:
            return None, i
