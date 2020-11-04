from .cnf import *
from os.path import isfile, join
from structure.array import Interval

SecretKey = Interval
PublicKey = Interval
KeyStream = Interval


class Instance:
    tag = None
    type = None
    path = None
    name = 'Instance'

    def __init__(self,
                 secret_key: SecretKey
                 ):
        self.secret_key = secret_key

    def __str__(self):
        return self.name

    def cnf(self):
        tag = self.tag if self.type is None else '%s_%s' % (self.tag, self.type)
        return CNF.parse(self.path, tag)

    def clauses(self):
        return self.cnf().clauses

    def check(self):
        return isfile(self.path)

    @staticmethod
    def has_intervals():
        return False

    def intervals(self):
        return []

    @staticmethod
    def build_path(*args):
        base = './instance/cnf/template'
        return join(base, *args) + '.cnf'


class Cipher(Instance):
    tag = None
    path = None
    name = 'Cipher'

    def __init__(self,
                 secret_key: SecretKey,
                 key_stream: KeyStream
                 ):
        super().__init__(secret_key)
        self.key_stream = key_stream

    @staticmethod
    def has_intervals():
        return True

    def intervals(self):
        return [self.key_stream]


StreamCipher = Cipher


class BlockCipher(Cipher):
    def __init__(self,
                 secret_key: SecretKey,
                 public_key: PublicKey,
                 key_stream: KeyStream
                 ):
        super().__init__(secret_key, key_stream)
        self.public_key = public_key

    def intervals(self):
        return [self.public_key, self.key_stream]


__all__ = [
    'Cipher',
    'Instance',
    'SecretKey',
    'PublicKey',
    'KeyStream',
    'BlockCipher',
    'StreamCipher'
]
