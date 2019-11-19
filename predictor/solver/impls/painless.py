from ..solver import *
from predictor.util.const import in_out_tools as iot


class PainLeSS(Solver):
    tag = 'painless'
    name = 'Solver: PainLeSS'
    script = './untar_painless.sh'
    statuses = {
        'SATISFIABLE': True,
        'UNSATISFIABLE': False,
        'UNKNOWN': None
    }
    min_time = 0.01

    def get_args(self, tl: int) -> List[str]:
        workers = 1
        l_args = ['python', iot['in'], self.solver_path, '-c=%d' % workers]

        if tl > 0:
            l_args.append('-t=%d' % tl)

        return l_args

    def parse_out(self, output):
        time = self.min_time
        status, solution = '', ''
        output = output.split('\n')
        for i in range(len(output)):
            if output[i].startswith('c s') or output[i].startswith('s'):
                status = output[i].split(' ')[-1]
            if output[i].startswith('c Resolution time: '):
                str_time = output[i].split(': ')[1]
                time = max(float(str_time[:-1]), self.min_time)
            if output[i].startswith('v'):
                solution_line = output[i].split(' ')
                for var in solution_line[1:]:
                    solution += '%s ' % var

        if status == '':
            return SolverReport(self.statuses['UNKNOWN'], -1)

        report = SolverReport(self.statuses[status], time)
        if self.statuses[status]:
            report.parse_solution(solution[:-1], self.spaces)

        return report


__all__ = [
    'PainLeSS'
]
