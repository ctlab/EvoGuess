from predictor.concurrency.task import Task
from predictor.method.method import Predictor
from predictor.util.environment import environment as env


class InverseBackdoorSets(Predictor):
    type = 'ibs'

    def __init__(self, **kwargs):
        Predictor.__init__(self, **kwargs)
        self.corrector = kwargs.get('corrector')

    def __init_phase(self, count, solver):
        env.out.debug(1, 0, 'generating init cases...')

        init_tasks = []
        for i in range(count):
            init_task = Task(
                init=True,
                solver=solver,
                case_f=env.case_generator.get_init()
            )
            init_tasks.append(init_task)

        solutions, init_time = env.concurrency.solve(init_tasks)
        env.out.debug(1, 0, 'has been solved %d init cases' % len(solutions))
        if count != len(solutions):
            env.out.debug(0, 0, 'warning! count != len(init_solved)')

        return solutions, init_time

    def __main_phase(self, backdoor, inited, solver):
        env.out.debug(1, 0, 'generating main cases...')

        main_tasks = []
        for _, _, solution in inited:
            main_case_f = env.case_generator.get_main(backdoor, solution)
            main_task = Task(
                solver=solver,
                case_f=main_case_f
            )
            main_tasks.append(main_task)

        env.out.debug(1, 0, 'solving...')
        solved, time = env.concurrency.solve(main_tasks, solver.get('workers'))
        env.out.d_debug(1, 0, 'has been solved %d cases' % len(solved))
        if len(inited) != len(solved):
            env.out.debug(0, 0, 'warning! len(init_solved) != len(solved)')

        return solved, time

    def compute(self, backdoor, cases, count, **kwargs):
        init, main = env.solvers['init'], env.solvers['main']
        env.out.d_debug(1, 0, 'compute for backdoor: %s' % backdoor)
        env.out.d_debug(1, 0, 'use time limit: %s' % main.get('tl'))

        all_time = 0
        while len(cases) < count:
            all_case_count = count - len(cases)

            if all_case_count > self.chunk_size:
                case_count = self.chunk_size
            else:
                case_count = all_case_count

            inited, init_time = self.__init_phase(case_count, init)
            solved, time = self.__main_phase(backdoor, inited, main)

            cases.extend(solved)
            all_time += init_time + time

        env.out.debug(1, 0, 'spent time: %f' % all_time)
        return cases, all_time

    def calculate(self, backdoor, compute_out):
        cases, time = compute_out

        env.out.debug(1, 0, 'counting time stat...')
        time_stat, log = self.get_time_stat(cases)
        env.out.d_debug(1, 0, 'time stat: %s' % time_stat)

        tl = env.solvers['main'].get('tl')
        if self.corrector is not None:
            env.out.debug(1, 0, 'correcting time limit...')
            tl, dis_count = self.corrector.correct(cases, tl)
            log += 'corrected time limit: %f\n' % tl
            env.out.d_debug(1, 0, 'new time limit: %f' % tl)

            env.out.debug(1, 0, 'correcting time stat...')
            time_stat['DISCARDED'] = dis_count
            time_stat['DETERMINATE'] -= dis_count
            env.out.d_debug(1, 0, 'new time stat: %s' % time_stat)

        log += 'spent time: %f\n' % time
        env.out.debug(1, 0, 'calculating value...')
        xi = float(time_stat['DETERMINATE']) / float(len(cases))
        if xi != 0:
            value = (2 ** len(backdoor)) * tl * (3 / xi)
        else:
            value = (2 ** env.algorithm.secret_key_len) * tl
        env.out.debug(1, 0, 'value: %.7g' % value)

        log += '%s\n' % time_stat
        return value, log, cases
