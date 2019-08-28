import warnings

from ..solver import Solver
from ..report import SolverReport


class RokkSolver(Solver):
    statuses = {
        "SATISFIABLE": "SATISFIABLE",
        "UNSATISFIABLE": "UNSATISFIABLE",
        "UNKNOWN": "INDETERMINATE"
    }

    min_time = 0.01

    def __init__(self, **kwargs):
        info = {
            "name": "rokk",
            "script": "./untar_rokk.sh"
        }
        Solver.__init__(self, info, **kwargs)

    def get_arguments(self, l_args, workers, tl, simp):
        l_args.append(self.solver_path)

        if tl > 0:
            l_args.append("-cpu-lim=%d" % tl)
        if workers != 1:
            warnings.warn("workers not support in rokk", UserWarning)

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        status, time, solution = "", self.min_time, ""
        for i in range(len(output)):
            if output[i].startswith("c s") or output[i].startswith("s"):
                status = output[i].split(' ')[-1]
            if output[i].startswith("c CPU time"):
                str_time = output[i].split(": ")[1]
                time = max(float(str_time[:-1]), self.min_time)
            if output[i].startswith("v"):
                solution_line = output[i].split(' ')
                for var in solution_line[1:]:
                    solution += "%s " % var

        report = SolverReport(self.statuses[status], time)
        if status == self.statuses["SATISFIABLE"]:
            report.parse_solution(solution, self.spaces)

        return report
