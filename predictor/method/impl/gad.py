from predictor.concurrency.task import Task
from predictor.method.method import Predictor
from predictor.util.environment import environment as env


class GuessAndDetermine(Predictor):
    type = "gad"

    def __main_phase(self, backdoor, solution, count, solver):
        env.comm.debug(1, 0, "generating main cases...")

        main_tasks = []
        for i in range(count):
            main_case_f = env.case_generator.get_main(backdoor, solution, 'b')
            main_task = Task(
                solver=solver,
                case_f=main_case_f
            )
            main_tasks.append(main_task)

        env.comm.debug(1, 0, "solving...")
        solved, time = env.concurrency.solve(main_tasks, solver.get('workers'))

        env.comm.d_debug(1, 0, "has been solved %d cases" % len(solved))
        if count != len(solved):
            env.comm.d_debug(0, 0, "warning! count != len(solved)")
        env.comm.debug(1, 0, "spent time: %f" % time)

        return solved, time

    def compute(self, backdoor, cases, count):
        env.comm.debug(1, 0, "compute for backdoor: %s" % backdoor)

        # init
        init_task = Task(
            init=True,
            solver=env.solvers['main'],
            substitutions=env.case_generator.get_init(),
        )

        _, _, solution = init_task.solve()

        all_time, solver = 0, env.solvers['main']
        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            solved, time = self.__main_phase(backdoor, solution, case_count, solver)

            cases.extend(solved)
            all_time += time

        env.comm.debug(1, 0, "spent time: %f" % all_time)
        return cases, all_time

    def calculate(self, backdoor, compute_out):
        cases, time = compute_out

        env.comm.debug(1, 0, "counting time stat...")
        time_stat, cases_log = self.get_time_stat(cases)
        env.comm.d_debug(1, 0, "time stat: %s" % time_stat)

        log = cases_log
        log += "spent time: %f\n" % time

        env.comm.debug(1, 0, "calculating value...")
        time_sum = 0.
        for _, time in cases:
            time_sum += float(time)

        env.comm.debug(1, 0, "avg time: %f (%f / %d)" % (time_sum / len(cases), time_sum, len(cases)))
        value = (2 ** len(backdoor)) * time_sum / len(cases)
        env.comm.debug(1, 0, "value: %.7g\n" % value)

        log += "%s\n" % time_stat
        return value, log, cases
