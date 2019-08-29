import signal
from math import log

from time import sleep, time as now
from predictor.util.q_pool import QPool
from predictor.util.environment import environment as env


def task_function(task):
    return task.solve()


class LimitPool:
    def __init__(self, **kwargs):
        self.thread_count = kwargs["thread_count"]
        self.process_count = kwargs["thread_count"]
        self.pool = QPool(processes=self.process_count)

        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

        signal.signal(signal.SIGINT, self.__signal_handler)

    def __signal_handler(self, s, f):
        if self.pool is not None:
            self.pool.terminate()
            exit(s)

    def solve(self, tasks, complexity=1, limit=0):
        process_count, remainder = divmod(self.thread_count, complexity)

        if process_count == 0 or remainder != 0:
            raise Exception("Incorrect number of threads or workers")
        elif process_count != self.process_count:
            self.pool.terminate()
            del self.pool

        if self.pool is None:
            self.pool = QPool(processes=process_count)
            self.process_count = process_count

        res_list = []
        for task in tasks:
            res = self.pool.apply_async(task_function, (task,))
            res_list.append(res)

        start_work_time = now()
        solve_f = self.__solve if limit == 0 else self.__limit_solve
        result = solve_f(res_list, [], limit)

        left = len(tasks) - len(result)
        result.extend([('INDET', float("inf"), [])] * left)

        return result, now() - start_work_time

    def __solve(self, res_list, result, *args):
        while len(res_list) > 0:
            res_list[0].wait()

            i = 0
            while i < len(res_list):
                if res_list[i].ready():
                    res = res_list.pop(i)
                    if res.successful():
                        result.append(res.get())
                    else:
                        env.out.debug(0, 1, "Pool solving was completed unsuccessfully")
                        result.append(res.get())
                else:
                    i += 1

            env.out.debug(2, 3, "Already solved %d tasks" % len(result))

        return result

    def __limit_solve(self, res_list, result, limit):
        wait_time = log(limit, self.size) if self.size > 1 else limit
        env.out.debug(2, 3, "base wait time: %f" % wait_time)
        wait_times = [wait_time] * self.size

        sync_flag = False
        time_sum, downtime = 0., 0.
        while not sync_flag:
            sleep(wait_time)
            downtime += wait_time

            i, res_len = 0, len(res_list)
            while i < len(res_list):
                if res_list[i].ready():
                    res = res_list.pop(i)
                    if res.successful():
                        data = res.get()
                        time_sum += data[1]
                        result.append(data)
                    else:
                        env.out.debug(0, 1, "Pool solving was completed unsuccessfully")
                        result.append(('ERROR', float("inf"), []))
                else:
                    i += 1

            active_count = min(self.process_count, res_len)
            if res_len > len(res_list):
                left_count = max(0, active_count - (res_len - len(res_list)))
                active_count = min(self.process_count, len(res_list))
                downtime = downtime * left_count / active_count if active_count > 0 else 0

                wait_times[self.rank] = wait_times[self.rank] * len(res_list) / res_len
                wait_times[self.rank] = max(0.1, wait_times[self.rank])
                env.out.debug(2, 3, "Already solved %d tasks" % len(result))
                env.out.debug(3, 3, "New wait time: %f" % wait_times[self.rank])

            down_sum = downtime * active_count
            env.out.debug(3, 3, "Downtime (%d) sum: %f" % (active_count, down_sum))
            estimation = time_sum + 0.5 * down_sum

            times = self.comm.allgather([estimation, wait_times[self.rank]])
            spent_time = sum([time[0] for time in times])
            wait_times = [time[1] for time in times]
            wait_time = max(wait_times)
            env.out.debug(3, 3, "Use wait time: %f" % wait_times[self.rank])

            if spent_time > limit and active_count > 0:
                env.out.debug(2, 3, "Terminate pool (%.2f > %.2f)" % (spent_time, limit))
                self.terminate()
                del self.pool

                res_list.clear()
                active_count = 0
                wait_times[self.rank] = 0

            sync_flags = self.comm.allgather(not active_count)
            sync_flag = all(sync_flags)

        return result

    def terminate(self):
        self.pool.terminate()
