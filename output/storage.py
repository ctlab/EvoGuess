import os
import shutil

from datetime import datetime


class Storage:
    def __init__(self, **kwargs):
        self.base_path = kwargs["base_path"]
        self.log_name = kwargs["log_name"]
        self.debug_name = kwargs["debug_name"]
        self.src_dump = kwargs["src_dump"]

        self.name = "%s-?" % self.__now()
        self.paths = {}

    def create(self, **kwargs):
        key_generator = kwargs["key_generator"]
        conf_path = kwargs["conf_path"]
        description = kwargs["description"] if "description" in kwargs else ""

        self.paths["alg"] = "%s/%s" % (self.base_path, key_generator)
        self.paths["main"] = "%s/%s" % (self.paths["alg"], self.name)
        self.paths["src"] = "%s/src" % self.paths["main"]

        if not os.path.isdir(self.paths["alg"]):
            os.mkdir(self.paths["alg"])

        os.mkdir(self.paths["main"])
        if len(description) > 0:
            description += '\n' if description[-1] != '\n' else ''
            open("%s/DESCRIPTION" % self.paths["main"], 'w+').write(description)

        if len(self.src_dump) > 0:
            os.mkdir(self.paths["src"])

        shutil.copy(conf_path, self.paths["main"])
        for src_path in self.src_dump:
            shutil.copy(src_path, self.paths["src"])

    def get_log_path(self):
        return "%s/%s" % (self.paths["main"], self.log_name)

    def get_debug_path(self):
        return "%s/%s" % (self.paths["main"], self.debug_name)

    def close(self):
        if self.name.find("?") < 0:
            raise Exception("Storage already closed")

        new_name = self.name.replace("?", self.__now())
        new_path = "%s/%s" % (self.paths["alg"], new_name)
        os.rename(self.paths["main"], new_path)

        self.name = new_name
        self.paths["main"] = new_path
        self.paths["src"] = "%s/src" % new_path

    def __now(self):
        now = datetime.today()
        z = lambda n: ("0%s" if n <= 9 else "%s") % n

        date = "%s.%s.%s" % (now.year, z(now.month), z(now.day))
        time = "%s:%s:%s" % (z(now.hour), z(now.minute), z(now.second))
        return "%s_%s" % (date, time)
