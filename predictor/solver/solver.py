import os
import re
import subprocess
import threading
from time import time as now
from typing import List

from predictor.util.const import solver_paths

from predictor.solver.tools import *
from predictor.solver.models import *


class Solver:
    tag = None
    script = None
    name = 'Solver'

    def __init__(self, **kwargs):
        self.interrupter = kwargs['interrupter']
        self.workers = kwargs.get('workers', 1)
        self.attempts = kwargs.get('attempts', 5)

        # self.options = set()
        self.spaces = re.compile('[\t ]+')
        self.solver_path = solver_paths[self.tag]

    def get_args(self, tl: int) -> List[str]:
        raise NotImplementedError

    def parse(self, output: str) -> SolverReport:
        raise NotImplementedError

    # def tune(self, name, value):
    #     option = SolverOption(name, value)
    #     self.options.add(option)

    def solve(self, cnf):
        args = ArgsBuilder(self)
        self.interrupter.hang(args)

        report = None
        l_args = args.build()
        thread_name = threading.current_thread().name
        for i in range(self.attempts):
            if report is None or report.check():
                # env.out.debug(4, 2, "%s start solving %s case" % (thread_name, self.tag))
                st = now()
                sp = subprocess.Popen(l_args, encoding='utf8', stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, err = sp.communicate(cnf)
                time = now() - st
                if len(err) != 0 and not err.startswith('timelimit'):
                    # env.out.debug(1, 2, "%s didn't solve %s case:\n%s" % (thread_name, self.tag, err))
                    trace(thread_name, "Subprocess error", '-', output, err)

                try:
                    report = self.parse(output)
                    if report.status == "INDETERMINATE":
                        report.time = time
                except KeyError as e:
                    # env.out.debug(1, 2, "%s error while parsing %s case" % (thread_name, self.tag))
                    report = SolverReport("INDETERMINATE", time)

                    if len(output) > 0:
                        title = "Key error while parsing output"
                        trace(thread_name, title, '-', output, "%s\n\n%s" % (err, e))

                # env.out.debug(4, 2, "%s solved %s case with status: %s" % (thread_name, self.tag, report.status))
                if report.check():
                    title = "Error while parsing solution"
                    trace(thread_name, title, '-', output, "%s in %d attempt" % (report.status, i))

        if report.check():
            report = SolverReport("INDETERMINATE", self.interrupter.tl)

        return report

    def __str__(self):
        return self.name


__all__ = [
    'List',
    'Solver',
    'SolverReport'
]
