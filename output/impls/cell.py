from datetime import datetime as dt

from ..output import *

from os.path import join
from os import makedirs, mkdir, rename


class Cell(Output):
    def __init__(self, **kwargs):
        self.name = ''
        self.files = {}
        super().__init__(**kwargs)
        self.logger = kwargs['logger']
        self.debugger = kwargs['debugger']

    def open(self, **kwargs):
        makedirs(self.path, exist_ok=True)

        self.name = '%s-?' % self.__now()
        self.path = join(self.path, self.name)

        mkdir(self.path)
        if kwargs.get('description'):
            open(join(self.path, 'DESCR'), 'w+').write(kwargs['description'])

        self.files['log'] = kwargs.get('log_file') or 'log'
        self.logger.set_out(join(self.path, self.files['log']))
        self.files['debug'] = kwargs.get('debug_file') or 'debug'
        self.debugger.set_out(join(self.path, self.files['debug']))

        return self

    def log(self, *strs: Iterable[str]) -> None:
        self.logger.write(*strs)

    def debug(self, verb: int, level: int, *strs: Iterable[str]) -> None:
        self.debugger.write(verb, level, *strs)

    def close(self):
        if self.name.find('?') < 0:
            raise Exception('Cell already closed')

        timestamp = self.__now()
        new_name = self.name.replace('?', timestamp)
        new_path = self.path.replace(self.name, new_name)
        rename(self.path, new_path)

        self.path = new_path
        self.name = new_name

    def __now(self):
        now = dt.today()
        z = lambda n: ("0%s" if n <= 9 else "%s") % n

        date = "%s.%s.%s" % (now.year, z(now.month), z(now.day))
        time = "%s:%s:%s" % (z(now.hour), z(now.minute), z(now.second))
        return "%s_%s" % (date, time)


__all__ = [
    'Cell'
]
