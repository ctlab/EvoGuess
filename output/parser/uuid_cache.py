import json
import tarfile
from time import time as now
from os.path import join, sep


class UUIDCache:
    def __init__(self, path, name):
        self.archive, self.members = None, {}
        self.tar_path = join(path, '%s.tar.gz' % name)

        self.list = {}
        list_path = join(path, '%s.list' % name)
        with open(list_path, 'r') as f:
            for line in f.readlines():
                info = json.loads(line)
                self.list[info["key"]] = info

    def _lazy_load(self):
        if self.archive is not None:
            return

        timestamp = now()
        self.archive = tarfile.open(self.tar_path, 'r:gz')
        for member in self.archive.getmembers():
            uuid = member.name.split(sep)[-1]
            # todo: may be use key instead uuid
            self.members[uuid] = member
        print('Archive was lazy loaded in %.2f seconds' % (now() - timestamp))

    def load(self, key):
        info = self.list.get(key)
        if info is None: return None

        self._lazy_load()
        member = self.members.get(info['uuid'])
        if member is None: return None

        file = self.archive.extractfile(member)
        if file is None: return None

        content = file.read().decode('utf-8')
        return json.loads(content)


__all__ = [
    'UUIDCache'
]
