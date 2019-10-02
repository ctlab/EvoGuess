from ..solver import *
import platform


class Lingeling(Solver):
    tag = 'lingeling'
    name = 'Solver: Lingeling'
    script = './untar_lingeling.sh'
    statuses = {
        'SATISFIABLE': 'SATISFIABLE',
        'UNSATISFIABLE': 'UNSATISFIABLE',
        'UNKNOWN': 'INDETERMINATE'
    }
    min_time = 0.001

    def get_args(self, tl: int) -> List[str]:
        args = [self.solver_path]

        if tl > 0:
            args.append('-t' if platform.system() == 'Darwin' else '-T')
            args.append(str(tl))

        return args

    def parse(self, output: str) -> SolverReport:
        time = self.min_time
        status, solution = '', ''
        output = output.split('\n')
        for i in range(len(output)):
            if output[i].startswith('c s') or output[i].startswith('s'):
                status = output[i].split(' ')
                status = status[len(status) - 1]
            if output[i].startswith('v'):
                solution_line = output[i].split(' ')
                for i in range(1, len(solution_line)):
                    solution += solution_line[i] + ' '
            if output[i].startswith('c ='):
                str_time = self.spaces.split(output[i + 1])[1]
                time = max(time, float(str_time))

        solution = solution[:-1]

        report = SolverReport(self.statuses[status], time)
        if status == self.statuses['SATISFIABLE']:
            report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'Lingeling'
]
