from ..solver import *


class CryptoMiniSAT(Solver):
    tag = 'cryptominisat'
    name = 'Solver: CryptoMiniSAT'
    script = './untar_crypto.sh'
    statuses = {
        'SATISFIABLE': True,
        'UNSATISFIABLE': False,
        'INDETERMINATE': None
    }
    min_time = 0.01

    def get_args(self, tl: int) -> List[str]:
        workers = 1
        args = [self.solver_path, '-t', str(workers)]

        if tl > 0:
            args.append(['--maxtime', str(tl)])

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
            if output[i].startswith('c Total time'):
                str_time = output[i].split(': ')[1]
                time = max(float(str_time), self.min_time)

        solution = solution[:-1]

        report = SolverReport(self.statuses[status], time)
        if self.statuses[status]:
            report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'CryptoMiniSAT'
]
