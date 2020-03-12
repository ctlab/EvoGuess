from ..solver import *
import warnings


class Treengeling(Solver):
    tag = 'treengeling'
    name = 'Solver: Treengeling'
    script = './untar_lingeling.sh'
    statuses = {
        'SATISFIABLE': True,
        'UNSATISFIABLE': False,
        'UNKNOWN': None
    }
    min_time = 0.001

    def get_args(self, tl: int) -> List[str]:
        workers = 1
        args = [self.solver_path, '-t', str(workers)]

        if tl > 0:
            warnings.warn('Time limit not support in plingeling', UserWarning)

        return args

    def parse_out(self, output):
        time = self.min_time
        status, solution = '', ''
        output = output.split('\n')
        for i in range(len(output)):
            if output[i].startswith('c s ') or output[i].startswith('s '):
                status = output[i].split(' ')
                status = status[len(status) - 1]
            if output[i].startswith('v'):
                solution_line = output[i].split(' ')
                for j in range(1, len(solution_line)):
                    solution += solution_line[j] + ' '
            if output[i].startswith('c ='):
                str_time = self.spaces.split(output[i + 1])[5]
                time = max(time, float(str_time))

        solution = solution[:-1]

        report = SolverReport(self.statuses[status], time)
        if self.statuses[status]:
            report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'Treengeling'
]
