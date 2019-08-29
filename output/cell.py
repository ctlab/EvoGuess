from os import mkdir, rename
from datetime import datetime
from os.path import join, isdir


class OutputCell:
    def __init__(self, **kwargs):
        self.path = ''
        for path in [kwargs['base'], kwargs.get('conference', ''), kwargs['keygen']]:
            self.path = join(self.path, path)
            if not isdir(self.path): mkdir(self.path)

        if not isdir(self.path): mkdir(self.path)
        self.name = '%s-?' % self.__now()
        self.path = join(self.path, self.name)

        mkdir(self.path)
        if kwargs.get('description'):
            kwargs['description'] += '\n' if kwargs['description'][-1] != '\n' else ''
            open('%s/DESCRIPTION' % self.path, 'w+').write(kwargs['description'])

        self.log = kwargs['log']
        self.verb, self.debug = kwargs['debug']

    def output(self):
        return {
            'log': join(self.path, self.log),
            'debug': (self.verb, [join(self.path, d) for d in self.debug])
        }

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
        now = datetime.today()
        z = lambda n: ("0%s" if n <= 9 else "%s") % n

        date = "%s.%s.%s" % (now.year, z(now.month), z(now.day))
        time = "%s:%s:%s" % (z(now.hour), z(now.minute), z(now.second))
        return "%s_%s" % (date, time)
