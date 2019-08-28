import os
import signal
import subprocess

from multiprocessing import Process
from multiprocessing.pool import Pool


class QProcess(Process):
    def terminate(self):
        spc = subprocess.Popen("pgrep -P %d" % self.pid, shell=True, stdout=subprocess.PIPE, encoding='utf8')
        ps_out = spc.stdout.read()
        spc.wait()
        for pid in ps_out.strip().split("\n"):
            try:
                os.kill(int(pid), signal.SIGTERM)
            except Exception:
                pass
        super(QProcess, self).terminate()


class QPool(Pool):
    def Process(self, *args, **kwargs):
        return QProcess(*args, **kwargs)
