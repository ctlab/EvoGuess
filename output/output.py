from time import sleep
from os.path import join
from datetime import datetime
from os import makedirs, mkdir, rename
from typing import Iterable

CREATED = 'CREATED'
OPENED = 'OPENED'
CLOSED = 'CLOSED'


class NotOpenedError(Exception):
    """The Output hasn't open yet."""
    pass


class AlreadyOpenedError(Exception):
    """The Output already opened."""
    pass


class AlreadyClosedError(Exception):
    """The Output already closed."""
    pass


def dt_now():
    now = datetime.today()
    z = lambda n: ('0%s' if n <= 9 else '%s') % n

    date = '%s.%s.%s' % (now.year, z(now.month), z(now.day))
    time = '%s:%s:%s' % (z(now.hour), z(now.minute), z(now.second))
    return '%s_%s' % (date, time)


class Output:
    name = 'Output'

    def __init__(self, path, **kwargs):
        self.path = path
        self.counter = -1
        self.kwargs = kwargs
        self.status = CREATED

        self._log_path = None
        self._debug_path = None
        self._extra_paths = []

        self._debug_verbosity = kwargs.get('dverb', 0)

    def _mkroot(self):
        try:
            name = '%s-?' % dt_now()
            path = join(self.path, name)
            mkdir(path)

            self.name = name
            self.path = path
            return True
        except FileExistsError:
            return False

    def open(self):
        if self.status != CREATED:
            raise AlreadyOpenedError()

        makedirs(self.path, exist_ok=True)
        while not self._mkroot():
            sleep(1)

        self.status = OPENED
        return self

    def close(self):
        if self.status != OPENED:
            raise AlreadyClosedError()

        new_name = self.name.replace('?', dt_now())
        new_path = self.path.replace(self.name, new_name)
        rename(self.path, new_path)

        self.path = new_path
        self.name = new_name
        self.status = CLOSED
        return self

    def register(self, extra_path):
        if self.status == CREATED:
            raise NotOpenedError()

        path = join(self.path, extra_path)
        makedirs(path, exist_ok=True)
        self._extra_paths.append(extra_path)
        return len(self._extra_paths) - 1

    def info(self, *strings: Iterable[str]):
        if self.status == CREATED:
            raise NotOpenedError()

        info_path = join(self.path, 'INFO')
        with open(info_path, 'w+') as f:
            f.writelines(list(strings))
        return self

    def is_open(self):
        if self.status == CREATED:
            raise NotOpenedError()
        if self.status == CLOSED:
            raise AlreadyClosedError()

    def touch(self):
        self.is_open()
        self.counter += 1

        lfile = self.kwargs.get('lfile', 'log')
        log_file = '%s_%d' % (lfile, self.counter)
        self._log_path = join(self.path, log_file)
        open(self._log_path, 'w+').close()

        dfile = self.kwargs.get('dfile', 'debug')
        debug_file = '%s_%d' % (dfile, self.counter)
        self._debug_path = join(self.path, debug_file)
        open(self._debug_path, 'w+').close()
        return self

    def log(self, *strings: Iterable[str]):
        self.is_open()
        with open(self._log_path, 'a') as f:
            f.writelines(list('%s\n' % s for s in strings))
        return self

    def debug(self, verbosity: int, level: int, *strings: Iterable[str]):
        if self._debug_verbosity >= verbosity:
            self.is_open()
            prefix = [str(datetime.today()), '--' * level]
            prefix_str = ' '.join(s for s in prefix if len(s))
            with open(self._debug_path, 'a') as f:
                f.writelines(['%s %s\n' % (prefix_str, s) for s in strings])
        return self

    def store(self, index, file, *strings):
        if self.status == CREATED:
            raise NotOpenedError()

        extra_path = self._extra_paths[index]
        store_path = join(self.path, extra_path, file)
        with open(store_path, 'a') as f:
            f.writelines(list('%s\n' % s for s in strings))

    def error(self, module, text, e):
        error_path = join(self.path, 'ERRORS')
        with open(error_path, 'a+') as f:
            f.write('%s: %s (%s)' % (module, text, e))
        return self


__all__ = [
    'Output'
]
