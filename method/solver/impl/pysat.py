from ..solver import *

from pysat import solvers
from threading import Timer
from time import time as now

saved_solvers = {}


class PySat(Solver):
    name = 'Solver'
    constructor = None

    def __init__(self, key=None):
        self._key = key

    def solve(self, clauses, assumptions, limit=0, ignore_key=False):
        saved = not ignore_key and self._key is not None
        if saved and self._key in saved_solvers:
            solver = saved_solvers[self._key]
            from_saved = True
        else:
            solver = self.constructor(bootstrap_with=clauses, use_timer=True)
            from_saved = False

            if saved:
                saved_solvers[self._key] = solver

        if limit > 0:
            timer = Timer(limit, solver.interrupt, ())
            timer.start()

            timestamp = now()
            status = solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
            full_time, time = now() - timestamp, solver.time()

            if timer.is_alive():
                timer.cancel()
            else:
                solver.clear_interrupt()
        else:
            timestamp = now()
            status = solver.solve(assumptions=assumptions)
            full_time, time = now() - timestamp, solver.time()

        solution = solver.get_model() if status else None
        statistics = solver.accum_stats()

        statistics['time'] = time
        if self._key is None:
            solver.delete()

        return status, statistics, solution, from_saved

    @staticmethod
    def delete(key: str):
        if key in saved_solvers:
            del saved_solvers[key]
            return True

        return False


#
# ----------------------------------------------------------------
#

class Cadical(PySat):
    name = 'Solver: Cadical'
    constructor = solvers.Cadical


class Glucose3(PySat):
    name = 'Solver: Glucose3'
    constructor = solvers.Glucose3


class Glucose4(PySat):
    name = 'Solver: Glucose4'
    constructor = solvers.Glucose4


class Lingeling(PySat):
    name = 'Solver: Lingeling'
    constructor = solvers.Lingeling


class MapleChrono(PySat):
    name = 'Solver: MapleChrono'
    constructor = solvers.MapleChrono


class MapleCM(PySat):
    name = 'Solver: MapleCM'
    constructor = solvers.MapleCM


class MapleSAT(PySat):
    name = 'Solver: MapleSAT'
    constructor = solvers.Maplesat


class Minicard(PySat):
    name = 'Solver: Minicard'
    constructor = solvers.Minicard


class Minisat22(PySat):
    name = 'Solver: Minisat22'
    constructor = solvers.Minisat22


class MinisatGH(PySat):
    name = 'Solver: MinisatGH'
    constructor = solvers.MinisatGH


solvers_dict = {
    'cd': Cadical,
    'g3': Glucose3,
    'g4': Glucose4,
    'lgl': Lingeling,
    'mcb': MapleChrono,
    'mcm': MapleCM,
    'mpl': MapleSAT,
    'mc': Minicard,
    'm22': Minisat22,
    'mgh': MinisatGH,
}


def get(key):
    return solvers_dict[key]()


__all__ = [
    'get',
    'Cadical',
    'Glucose3',
    'Glucose4',
    'Lingeling',
    'MapleChrono',
    'MapleCM',
    'Minicard',
    'Minisat22',
    'MinisatGH'
]
