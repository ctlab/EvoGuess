from ..solver import Solver
from ..report import SolverReport


class CryptoMinisatSolver(Solver):
    statuses = {
        "SATISFIABLE": "SATISFIABLE",
        "UNSATISFIABLE": "UNSATISFIABLE",
        "INDETERMINATE": "INDETERMINATE"
    }

    min_time = 0.01

    def __init__(self, **kwargs):
        info = {
            "name": "cryptominisat",
            "script": "./untar_crypto.sh"
        }
        Solver.__init__(self, info, **kwargs)

    def get_arguments(self, l_args, workers, tl, simp):
        l_args.extend([self.solver_path, "-t", str(workers)])

        if tl > 0:
            l_args.extend(["--maxtime", "%d" % tl])

        return l_args

    def parse_out(self, output):
        output = output.split('\n')
        solution = ""
        status = ""
        time = self.min_time
        for i in range(len(output)):
            if output[i].startswith("c s") or output[i].startswith("s"):
                status = output[i].split(' ')
                status = status[len(status) - 1]
            if output[i].startswith("v"):
                solution_line = output[i].split(' ')
                for i in range(1, len(solution_line)):
                    solution += solution_line[i] + " "
            if output[i].startswith("c Total time"):
                str_time = output[i].split(": ")[1]
                time = max(float(str_time), self.min_time)

        solution = solution[:-1]

        report = SolverReport(self.statuses[status], time)
        if status == self.statuses["SATISFIABLE"]:
            report.parse_solution(solution, self.spaces)

        return report
