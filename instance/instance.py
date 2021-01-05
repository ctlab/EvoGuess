from .cnf import *

from os.path import isfile, join
from structure.array import Interval
from utils import numeral_system as ns

SecretKey = Interval
PublicKey = Interval
KeyStream = Interval

base_path = './instance/cnf/template'


class Instance:
    tag = None
    base = None
    type = None
    x_path = None
    cnf_path = None
    name = 'Instance'

    def __init__(self,
                 secret_key: SecretKey
                 ):
        self.secret_key = secret_key
        self.key = self.tag if self.type is None else '%s_%s' % (self.tag, self.type)

    def __str__(self):
        return self.name

    def cnf(self):
        return CNF.parse(self.cnf_path, self.key)

    def clauses(self):
        return self.cnf().clauses

    def check(self):
        return isfile(self.cnf_path)

    def get_assumptions(self, bits):
        variables = self.secret_key.filter(bits[0])
        values = ns.binary_to_base(self.base, bits[1])
        # todo: convert bits[2:] to base values
        assert len(variables) == len(values)

        if self.base > 2:
            x_map = XMAP.parse(self.x_path, self.key)
            assumptions = map(x_map.get_cnf_var, variables, values)
        else:
            assumptions = [x if values[i] else -x for i, x in enumerate(variables)]

        # todo: add intervals to assumptions
        return assumptions

    @staticmethod
    def has_intervals():
        return False

    def intervals(self):
        return []

    @staticmethod
    def build_cnf_path(*args):
        return join(base_path, *args) + '.cnf'

    @staticmethod
    def build_x_map_path(*args):
        return join(base_path, *args) + '-x.pickle'


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
