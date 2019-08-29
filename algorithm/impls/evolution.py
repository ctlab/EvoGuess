import numpy as np
from copy import copy
from time import time as now

from algorithm.algorithm import Algorithm


class EvolutionAlgorithm(Algorithm):
    name = "evolution"

    def __init__(self, **kwargs):
        Algorithm.__init__(self, **kwargs)
        self.strategy = kwargs["strategy"]
        self.mutation = kwargs["mutation"]
        self.crossover = kwargs["crossover"]

        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

    def start(self, backdoor, **env):
        start_time = now()
        env['out'].debug(0, 0, "Evolution start on %d nodes" % self.size)

        if self.rank == 0:
            self.condition.set("stagnation", 1)
            max_value = float("inf")
            updated_logs = {}

            P = self.__restart(backdoor)
            if str(backdoor) in env['values']:
                env['best'] = (backdoor, env['values'][str(backdoor)][0], [])
            else:
                env['best'] = (backdoor, max_value, [])
            locals_list = []

            while not self.condition.check():
                self.print_iteration_header(self.condition.get("iteration"))
                P_v = []
                for p in P:
                    key = str(p)
                    if key in env['values']:
                        hashed = True
                        if key in updated_logs:
                            logs = updated_logs[key]
                            updated_logs.pop(key)
                        else:
                            logs = ""

                        (value, _), pf_log = env['values'][key], logs

                        p_v = (p, value)
                    else:
                        hashed = False
                        start_work_time = now()

                        env['out'].debug(2, 1, "sending backdoor... %s" % p)
                        self.comm.bcast(p.pack(), root=0)
                        c_out = predictive_f.compute(p)

                        cases = self.comm.gather(c_out[0], root=0)
                        env['out'].debug(2, 1, "been gathered cases from %d nodes" % len(cases))
                        cases = np.concatenate(cases)

                        time = now() - start_work_time
                        r = predictive_f.calculate(p, (cases, time))

                        value, pf_log = r[0], r[1]
                        self.condition.increase("pf_calls")
                        env['values'][key] = value, len(cases)
                        p_v = (p, value)

                        if self.comparator.compare(env['best'], p_v) > 0:
                            env['best'] = p_v
                            self.condition.set("stagnation", -1)

                    P_v.append(p_v)
                    self.print_pf_log(hashed, key, value, pf_log)

                self.condition.increase("stagnation")
                P_v.sort(cmp=self.comparator.compare)
                P = self.strategy.get_next_P((self.mutation.mutate, self.crossover.cross), P_v)

                self.condition.increase("iteration")
                self.condition.set("time", now() - start_time)

            self.comm.bcast([-1, True], root=0)

            if env['best'][1] != max_value:
                locals_list.append(env['best'])
                self.condition.increase("locals")
                self.print_local_info(env['best'])

            return locals_list
        else:
            while True:
                array = self.comm.bcast(None, root=0)
                if array[0] == -1:
                    break

                p = Backdoor.unpack(array)
                env['out'].debug(2, 1, "been received backdoor: %s" % p)
                c_out = predictive_f.compute(p)

                env['out'].debug(2, 1, "sending %d cases... " % len(c_out[0]))
                self.comm.gather(c_out[0], root=0)

    def get_info(self):
        info = Algorithm.get_info(self)
        info += "-- %s\n" % str(self.strategy)
        info += "-- %s\n" % str(self.mutation)
        info += "-- %s\n" % str(self.crossover)
        return info

    def __restart(self, backdoor):
        P = []
        for i in range(self.strategy.get_P_size()):
            P.append(copy(backdoor))

        return P
