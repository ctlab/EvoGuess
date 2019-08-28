import warnings

from ..solver import Solver
from ..report import SolverReport


class CadicalSolver(Solver):
    statuses = {
        "SATISFIABLE": "SATISFIABLE",
        "UNSATISFIABLE": "UNSATISFIABLE",
        "UNKNOWN": "INDETERMINATE"
    }

    min_time = 0.001

    def __init__(self, **kwargs):
        info = {
            "name": "cadical",
            "script": "./untar_cadical.sh"
        }
        Solver.__init__(self, info, **kwargs)

    def get_arguments(self, l_args, workers, tl, simp):
        l_args.append(self.solver_path)

        if tl > 0:
            l_args.extend(["-t", "%d" % tl])
        if workers != 1:
            warnings.warn("workers not support in cadical", UserWarning)

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        solution = ""
        status = ""
        time = self.min_time
        for i in range(len(output)):
            if output[i].startswith("c s ") or output[i].startswith("s"):
                status = output[i].split(' ')
                status = status[len(status) - 1]
            if output[i].startswith("v"):
                solution_line = output[i].split(' ')
                for i in range(1, len(solution_line)):
                    solution += solution_line[i] + " "
            if output[i].startswith("c total process time"):
                str_time = self.spaces.split(output[i])[-2]
                time = max(time, float(str_time))

        solution = solution[:-1]

        report = SolverReport(self.statuses[status], time)
        if status == self.statuses["SATISFIABLE"]:
            report.parse_solution(solution, self.spaces)

        return report
