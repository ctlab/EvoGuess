import os
import signal
import subprocess

from multiprocessing import Process


class SolverProcess(Process):
    def terminate(self):
        spc = subprocess.Popen("pgrep -P %d" % self.pid, shell=True, encoding='utf8', stdout=subprocess.PIPE)
        ps_out = spc.stdout.read()
        spc.wait()
        for pid in ps_out.strip().split("\n"):
            try:
                os.kill(int(pid), signal.SIGTERM)
            except Exception:
                pass
        super().terminate()


__all__ = [
    'SolverProcess'
]
