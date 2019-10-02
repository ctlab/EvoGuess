from ..solver import *


class MapleSAT(Solver):
    tag = 'maplesat'
    name = 'Solver: MapleSAT'
    script = './untar_maplesat.sh'
    statuses = {
        'SATISFIABLE': 'SATISFIABLE',
        'UNSATISFIABLE': 'UNSATISFIABLE',
        'UNKNOWN': 'INDETERMINATE'
    }
    min_time = 0.01

    def get_args(self, tl: int) -> List[str]:
        args = [self.solver_path]

        if tl > 0:
            args.append('-cpu-lim=%d' % tl)

        return args

    def parse(self, output: str) -> SolverReport:
        output = output.split('\n')
        i = 0
        while not output[i].startswith('CPU time'):
            i += 1

        str_time = output[i].split(': ')[1]
        time = max(float(str_time[:-1]), self.min_time)

        status = output[i + 2]

        report = SolverReport(self.statuses[status], time)
        # if status == self.statuses['SATISFIABLE']:
        #     report.parse_solution(solution, self.spaces)

        return report


__all__ = [
    'MapleSAT'
]

# |  Number of variables:          4010                                         |
# |  Number of clauses:           17658                                         |
# |  Parse time:                   0.01 s                                       |
# |  Eliminated clauses:           0.43 Mb                                      |
# |  Simplification time:          0.05 s                                       |
# |                                                                             |
# LBD Based Clause Deletion : 1
# Rapid Deletion : 1
# Almost Conflict : 1
# Anti Exploration : 1
# ============================[ Search Statistics ]==============================
# | Conflicts |          ORIGINAL         |          LEARNT          | Progress |
# |           |    Vars  Clauses Literals |    Limit  Clauses Lit/Cl |          |
# ===============================================================================
# ===============================================================================
# restarts              : 1
# conflicts             : 0              (0 /sec)
# decisions             : 1              (0.00 % random) (17 /sec)
# propagations          : 0              (0 /sec)
# conflict literals     : 0              (-nan % deleted)
# actual reward         : -nan
# Memory used           : 9.00 MB
# CPU time              : 0.058991 s
#
# SATISFIABLE
