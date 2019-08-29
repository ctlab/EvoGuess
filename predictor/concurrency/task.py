from predictor.util.environment import environment as env


class Task:
    def __init__(self, **kwargs):
        self.case_f = kwargs['case_f']
        self.solver = kwargs['solver']
        self.init = 'init' in kwargs

    def solve(self):
        case = self.case_f()
        try:
            report = self.solver.solve(case.get_cnf())
            case.mark_solved(report)
            if self.init: case.check_solution()
        except Exception as e:
            env.out.debug(0, 2, 'error while solving case:\n%s' % e)

        solution = case.solution if self.init else []
        return case.get_status(short=True), case.time, solution
