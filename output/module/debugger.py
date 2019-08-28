import threading
import os

from datetime import datetime


class Debugger:
    def __init__(self, path, verb=0):
        self.path = path
        # if not os.path.isfile(path):
        open(path, 'w+').close()
        self.verb = verb
        self.queue = []
        self.lock = threading.Lock()

    def deferred_write(self, verb, level=0, *strs):
        if self.verb < verb:
            return

        self.lock.acquire()
        self.queue.append(self.__prepare_str(level, *strs))
        self.lock.release()

    def write(self, verb, level=0, *strs):
        if self.verb < verb and len(self) == 0:
            return

        self.lock.acquire()
        with open(self.path, 'a') as f:
            map(f.write, self.queue)
            self.queue.clear()

            if self.verb >= verb:
                f.write(self.__prepare_str(level, *strs))
        self.lock.release()

    def __len__(self):
        return len(self.queue)

    def __prepare_str(self, level, *strs):
        s = ' '.join(strs)
        ss = ['(%s) %s %s\n' % (datetime.today(), self.__lp(level), line) for line in s.split('\n')]
        s = ''.join(ss)
        return s

    def __lp(self, level):
        return '--' * level


class DebuggerStub:
    def __init__(self):
        pass

    def deferred_write(self, verb, level=0, *strs):
        pass

    def write(self, verb, level=0, *strs):
        pass


def get_debugger(path, verb=0):
    return Debugger(path, verb) if len(path) > 0 else DebuggerStub()
