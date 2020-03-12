from ..solver import *


class RoKK(Solver):
    tag = 'rokk'
    name = 'Solver: RoKK'
    script = './untar_rokk.sh'
    statuses = {
        'SATISFIABLE': True,
        'UNSATISFIABLE': False,
        'UNKNOWN': None
    }
    min_time = 0.01

    def get_args(self, tl: int) -> List[str]:
        args = [self.solver_path]

        if tl > 0:
            args.append('-cpu-lim=%d' % tl)

        return args

    def parse(self, output: str) -> SolverReport:
        time = self.min_time
        status, solution = '', ''
        output = output.split('\n')
        for i in range(len(output)):
            if output[i].startswith('c s') or output[i].startswith('s'):
                status = output[i].split(' ')[-1]
            if output[i].startswith('c CPU time'):
                str_time = output[i].split(': ')[1]
                time = max(float(str_time[:-1]), self.min_time)
            if output[i].startswith('v'):
                solution_line = output[i].split(' ')
                for var in solution_line[1:]:
                    solution += '%s ' % var

        report = SolverReport(self.statuses[status], time)
        if self.statuses[status]:
            report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'RoKK'
]
