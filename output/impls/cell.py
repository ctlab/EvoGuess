from ..output import *

from time import sleep
from os.path import join, exists
from datetime import datetime as dt
from os import makedirs, mkdir, rename


class Cell(Output):
    def __init__(self, **kwargs):
        self.name = ''
        self.count = 0
        super().__init__(**kwargs)

        self.tries = kwargs.get('tries', 50)

    def open(self, **kwargs):
        if self.rank == 0:
            makedirs(self.path, exist_ok=True)

            tries = 0
            name = '%s-?' % self.__now()
            path = join(self.path, name)
            while tries < self.tries:
                tries += 1
                try:
                    mkdir(path)
                    break
                except FileExistsError:
                    sleep(1)
                    name = '%s-?' % self.__now()
                    path = join(self.path, name)

            self.name = name
            self.path = path
            if kwargs.get('description'):
                open(join(self.path, 'DESCR'), 'w+').write(kwargs['description'])

        if self.size > 1:
            self.path = self.comm.bcast(self.path, root=0)

        return self

    def touch(self, **kwargs):
        lfile = kwargs.get('lfile', 'log')
        dfile = kwargs.get('dfile', 'debug')

        log_file = '%s_%d' % (lfile, self.count)
        debug_file = '%s_%d_%d' % (dfile, self.count, self.rank)
        self.logger.set_out(join(self.path, log_file))
        self.debugger.set_out(join(self.path, debug_file))
        self.count += 1

        return self

    # def child(self):
    #     if self.rank == 0:
    #         log_file = '%s_%s' % (self.files['log'], self.count)
    #         debug_file = '%s_%s' % (self.files['debug'], self.count)
    #         self.logger.set_out(join(self.path, log_file))
    #         self.debugger.set_out(join(self.path, debug_file))
    #         self.count += 1
    #
    #     return self

    def close(self):
        if self.rank == 0:
            if self.name.find('?') < 0:
                raise Exception('Cell already closed')

            timestamp = self.__now()
            new_name = self.name.replace('?', timestamp)
            new_path = self.path.replace(self.name, new_name)
            rename(self.path, new_path)

            self.path = new_path
            self.name = new_name

        return self

    def __now(self):
        now = dt.today()
        z = lambda n: ('0%s' if n <= 9 else '%s') % n

        date = '%s.%s.%s' % (now.year, z(now.month), z(now.day))
        time = '%s:%s:%s' % (z(now.hour), z(now.minute), z(now.second))
        return '%s_%s' % (date, time)


__all__ = [
    'Cell'
]
