import os
import threading


class Logger:
    def __init__(self, path):
        self.path = path
        # if not os.path.isfile(path):
        open(path, 'w+').close()
        self.queue = []
        self.lock = threading.Lock()

    def deferred_write(self, *strs):
        self.lock.acquire()
        self.queue.extend(map(self.__prepare_str, strs))
        self.lock.release()

    def write(self, *strs):
        self.lock.acquire()
        with open(self.path, "a") as f:
            map(f.write, self.queue)
            self.queue.clear()
            [f.write(self.__prepare_str(s)) for s in strs]
        self.lock.release()

    def __len__(self):
        return len(self.queue)

    def __prepare_str(self, s):
        return "%s\n" % s if s[-1] != '\n' else s


class LoggerStub:
    def __init__(self):
        pass

    def deferred_write(self, *strs):
        pass

    def write(self, *strs):
        pass


def get_logger(path):
    return Logger(path) if len(path) > 0 else LoggerStub()
