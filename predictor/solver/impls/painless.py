from ..solver import Solver
from ..report import SolverReport
from predictor.util.const import in_out_tools as iot


class PainlessSolver(Solver):
    statuses = {
        "SATISFIABLE": "SATISFIABLE",
        "UNSATISFIABLE": "UNSATISFIABLE",
        "UNKNOWN": "INDETERMINATE"
    }

    min_time = 0.01

    def __init__(self, **kwargs):
        info = {
            "name": "painless",
            "script": "./untar_painless.sh"
        }
        Solver.__init__(self, info, **kwargs)

    def get_arguments(self, args, workers, tl, simp):
        l_args = ["python", iot["in"]]
        l_args.extend(args)
        l_args.extend([self.solver_path, "-c=%d" % workers])

        if tl > 0:
            l_args.append("-t=%d" % tl)

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        status, time, solution = "", self.min_time, ""
        for i in range(len(output)):
            if output[i].startswith("c s") or output[i].startswith("s"):
                status = output[i].split(' ')[-1]
            if output[i].startswith("c Resolution time: "):
                str_time = output[i].split(": ")[1]
                time = max(float(str_time[:-1]), self.min_time)
            if output[i].startswith("v"):
                solution_line = output[i].split(' ')
                for var in solution_line[1:]:
                    solution += "%s " % var

        if status == "":
            return SolverReport(self.statuses["UNKNOWN"], -1)

        report = SolverReport(self.statuses[status], time)
        if status == self.statuses["SATISFIABLE"]:
            report.parse_solution(solution[:-1], self.spaces)

        return report
