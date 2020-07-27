import re

from ..parser import *
from method.concurrency.models import Result
from method.instance.models.var import Backdoor

statuses = {
    'SAT': True,
    'IND': None,
    'UNSAT': False
}


class LogParser(Parser):
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.hash = {}
        self.bd = re.compile(r'[\[\]]')
        self.res = re.compile(r'[() at]+')
        self.float = re.compile(r'[^\d.]+')

    def parse(self, data):
        info, i = [], 0
        while not data[i].startswith('---'):
            info.append(data[i])
            i += 1

        iterations = []
        iteration, i = self.parse_iteration(data, i + 1)
        while iteration is not None:
            iterations.append(iteration)
            iteration, i = self.parse_iteration(data, i)

        return info, iterations

    def parse_iteration(self, data, i):
        if len(data) <= i:
            return None, i

        if data[i].startswith('Iteration'):
            cases = []
            case, i = self.parse_case(data, i + 2)
            while case is not None:
                cases.append(case)
                case, i = self.parse_case(data, i)
            return cases, i
        else:
            return None, i

    def parse_case(self, data, i):
        if len(data) <= i:
            return None, i

        if data[i].startswith('Run'):
            backdoor = Backdoor.parse(self.bd.split(data[i])[1])

            results, j = [], 0
            result, i = self.parse_result(data, i + 2, j)
            while result is not None:
                j += 1
                results.append(result)
                result, i = self.parse_result(data, i, j)

            assert data[i].startswith('{')
            assert data[i + 1].startswith('Spent')
            cpu_time = float(self.float.sub('', data[i + 1]))
            assert data[i + 2].startswith('End')
            value = float(data[i + 2].split('value: ')[1])

            case = Case(backdoor, results, cpu_time).set(value)
            self.hash[str(backdoor)] = case
            return case, i + 4
        elif data[i].startswith('Hash'):
            backdoor = Backdoor.parse(self.bd.split(data[i])[1])
            case = self.hash[str(backdoor)].get_copy()
            return case, i + 3
        else:
            return None, i

    def parse_result(self, data, i, j):
        if ' at ' in data[i]:
            status, time, pid = self.res.split(data[i])
            result = Result(j, statuses[status], float(time), {}, None)
            result.pid = int(pid)
            return result, i + 1
        else:
            return None, i


__all__ = [
    'LogParser'
]
