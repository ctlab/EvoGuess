from ..algorithm import *
from ..models.rank_cases import RankCases

from time import time as now
from numpy import concatenate
from operator import itemgetter


class RankEvolution(Algorithm):
    name = 'Algorithm: Rank Evolution'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}
        self.rank_cache = {}
        self.strategy = kwargs['strategy']
        self.stat_test = kwargs['stat_test']
        self.stagnation_limit = kwargs['stagnation_limit']

    def process(self, backdoor: Backdoor) -> List[Individual]:
        timestamp = now()

        points = []
        self.log_info().log_delim()
        self.limit.set('stagnation', 0)

        root = Individual(backdoor)
        count = self.stat_test.step_size
        self.log_it_header(0, 'base').log_delim()
        start_work_time = now()
        estimation = self.predict(backdoor, count)
        for cases in estimation.cases:
            cases.pop(0)
        cases = concatenate(estimation.cases)
        self.method.log_run(backdoor, len(cases))
        info = self.method.function.calculate(backdoor, cases, **self.method.kwargs)
        time = now() - start_work_time
        self.method.log_end(cases, info, time)

        key = str(backdoor)
        self.cache[key] = (info.value, len(cases))
        tl = self.method.function.tl if hasattr(self.method.function, 'tl') else 0
        rank_cases = RankCases(backdoor, tl, cases)
        self.rank_cache[key] = rank_cases, 1., 1.
        best = root.set(info.value)
        self.log_delim()

        self.limit.set('iteration', 1)
        population = self.strategy.breed([best])
        self.limit.set('time', now() - timestamp)
        while not self.limit.exhausted():
            it = self.limit.get('iteration')
            self.log_it_header(it).log_delim()

            # self.method.switch(population) # todo: integrate

            start_work_time, repeats = now(), 0
            tasks = self.get_tasks(best, population)
            while len(tasks) > 0:
                for i in range(1, self.size):
                    backdoor, count = tasks[i]
                    self.output.debug(2, 1, 'Sending to %d backdoor... %s' % (i, backdoor))
                    self.comm.send([BTypes.ESTIMATE.value, count] + backdoor.snapshot(), dest=i)

                backdoor, count = tasks[0]
                estimation = self.method.estimate(backdoor, count=count)

                keys = set()
                for cases in estimation.cases:
                    i = cases.pop(0)
                    backdoor = tasks[i][0]
                    key = str(backdoor)
                    if key in self.rank_cache:
                        self.rank_cache[key][0].extend(cases)
                    else:
                        tl = self.method.function.tl if hasattr(self.method.function, 'tl') else 0
                        cases = RankCases(backdoor, tl, cases)
                        self.rank_cache[key] = cases, 1., 1.

                    keys.add(key)

                best_key = str(best.backdoor)
                for key in keys:
                    key_cases = self.rank_cache[key][0]
                    best_cases = self.rank_cache[best_key][0]
                    a, b = self.stat_test.test(best_cases, key_cases)
                    self.output.debug(0, 0, 'Test %s and %s' % (best_key, key))
                    debug_args = (len(best_cases), len(key_cases), a, b)
                    self.output.debug(0, 0, 'With length (%d) (%d): With values %.4f --- %.4f' % debug_args)
                    self.rank_cache[key] = key_cases, a, b

                repeats += 1
                tasks = self.get_tasks(best, population)

            self.output.debug(0, 0, 'End iteration after %d tasks' % repeats, '')
            time = now() - start_work_time

            for individual in population:
                backdoor = individual.backdoor
                key = str(backdoor)
                best_key = str(best.backdoor)

                cases = self.rank_cache[key][0].cases
                current_count = len(cases)
                if key not in self.cache:
                    self.limit.increase('predictions')
                    self.method.log_run(backdoor, current_count)
                    info = self.method.function.calculate(backdoor, cases, **self.method.kwargs)
                    self.method.log_end(cases, info, time)
                    self.cache[key] = (info.value, current_count)
                    individual.set(info.value)
                else:
                    value, count = self.cache[key]
                    if count < current_count:
                        self.method.log_run(backdoor, current_count)
                        info = self.method.function.calculate(backdoor, cases, **self.method.kwargs)
                        self.method.log_end(cases, info, time)
                        self.cache[key] = (info.value, current_count)
                        individual.set(info.value)
                    else:
                        self.method.log_cached(backdoor, value)
                        individual.set(value)

                self.log_delim()
                if key == best_key:
                    best = individual

            for individual in population:
                if best > individual:
                    best = individual
                    self.limit.set('stagnation', -1)

            # restart
            self.limit.increase('iteration')
            self.limit.increase('stagnation')
            if self.limit.get('stagnation') >= self.stagnation_limit:
                points.append(best)
                best = root
                self.limit.set('stagnation', 0)
                # info = self.strategy.configure(self.limit.limits)
                # self.output.debug(3, 1, 'configure: ' + str(info))
                population = self.strategy.breed([root])

                # create new log file
                if not self.limit.exhausted():
                    self.touch_log().log_info().log_delim()
            else:
                # info = self.strategy.configure(self.limit.limits)
                # self.output.debug(3, 1, 'configure: ' + str(info))
                population = self.strategy.breed(population)

            self.limit.set('time', now() - timestamp)

        if best.value < root.value:
            points.append(best)
            print('Local: %s' % best)

        self.log_delim()
        self.output.log('Points:')
        for point in points:
            self.output.log(str(point))

        return points

    def get_tasks(self, best, population):
        all_tasks = []
        keys = set()

        rtb = self.stat_test.bound
        step = self.stat_test.step_size
        bound = self.sampling.get_size(None)
        best_key = str(best.backdoor)
        for individual in population:
            key = str(individual.backdoor)
            if key not in keys:
                keys.add(key)
                if key not in self.rank_cache:
                    for _ in range(step, bound, step):
                        all_tasks.append((individual, bound + 1.))

                    all_tasks.append((individual, 0.))
                    continue

                cases, pv1, pv2 = self.rank_cache[key]
                if key != best_key:
                    if pv1 < rtb or pv2 < rtb:
                        continue
                else:
                    pv1, pv2 = 0., 0.

                for tick in range(len(cases), bound, step):
                    all_tasks.append((individual, tick + pv2))

        if len(all_tasks) < self.size:
            return []

        tasks = sorted(all_tasks, key=itemgetter(1))[:self.size]
        return [(task[0].backdoor, step) for task in tasks]

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            self.strategy,
            self.stat_test,
            'Stagnations: %d' % self.stagnation_limit,
        ]))


__all__ = [
    'RankEvolution'
]
