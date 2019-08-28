import warnings


class SolverReport:
    def __init__(self, status, time):
        self.time = time
        self.status = status
        self.solution = []
        self.flags = [
            False  # preprocessing
        ]

    def parse_solution(self, solution_str, spaces):
        solution_str = solution_str.strip()
        if len(solution_str) == 0:
            self.status = "BROKEN"
            warnings.warn("Solution string is empty", UserWarning)
            return

        data = spaces.split(solution_str)

        try:
            for var in data:
                i_var = int(var)
                if i_var < 0:
                    self.solution.append(0)
                elif i_var > 0:
                    self.solution.append(1)
        except ValueError:
            self.status = "BROKEN"
            warnings.warn("Error while parse solution", UserWarning)

    def set_flag(self, i, value):
        self.flags[i] = value

    def check(self):
        return self.status == "BROKEN"

    def __str__(self):
        return "%s (%f) with solution: %d" % (self.status, self.time, len(self.solution))
