from ..solver import *
from predictor.util.const import in_out_tools as iot


class MiniSAT(Solver):
    tag = 'minisat'
    name = 'Solver: MiniSAT'
    script = './untar_minisat.sh'
    statuses = {
        'SAT': True,
        'UNSAT': False,
        'INDET': None
    }
    min_time = 0.01

    def get_args(self, tl: int) -> List[str]:
        l_args = ['python', iot['both'], self.solver_path]

        if tl > 0:
            l_args.append('-cpu-lim=%d' % tl)

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        i, time = 0, self.min_time
        for i in range(len(output)):
            if output[i].startswith('CPU time'):
                time_str = ''
                for s in output[i].split(':')[1]:
                    if s.isdigit() or s == '.':
                        time_str += s
                time = max(time, float(time_str))
                break

        i += 1
        while not len(output[i]):
            i += 1
        status = output[i]
        solution = output[i + 2][:-1]

        report = SolverReport(status, time)
        if self.statuses[status]:
            report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'MiniSAT'
]
