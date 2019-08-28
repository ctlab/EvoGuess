import warnings

from ..solver import Solver
from ..report import SolverReport
from predictor.util.const import in_out_tools as iot


class MinisatSolver(Solver):
    statuses = {
        "SAT": "SATISFIABLE",
        "UNSAT": "UNSATISFIABLE",
        "INDET": "INDETERMINATE"
    }

    min_time = 0.01

    def __init__(self, **kwargs):
        info = {
            "name": "minisat",
            "script": "./untar_minisat.sh"
        }
        Solver.__init__(self, info, **kwargs)

    def get_arguments(self, args, workers, tl, simp):
        l_args = ["python", iot["both"]]
        l_args.extend(args)
        l_args.append(self.solver_path)

        if tl > 0:
            l_args.append("-cpu-lim=%d" % tl)
        if workers != 1:
            warnings.warn("workers not support in lingeling", UserWarning)

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        i, time = 0, self.min_time
        for i in range(len(output)):
            if output[i].startswith("CPU time"):
                time_str = ""
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
        if status == self.statuses["SAT"]:
            report.parse_solution(solution, self.spaces)

        return report
