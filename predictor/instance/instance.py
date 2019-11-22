from .models import *
from .models.var import *

from os.path import isfile


class Instance:
    tag = None
    path = None
    name = 'Instance'

    def __init__(self, **kwargs):
        self._cnf = None
        self.secret_key = kwargs['secret_key']

    def __str__(self):
        return self.name

    def clauses(self):
        if self._cnf is None:
            # print('parse cnf...')
            self._cnf = cnf.Cnf.parse(self.path)

        return self._cnf.clauses

    def cnf(self):
        if self._cnf is None:
            # print('parse cnf...')
            self._cnf = cnf.Cnf.parse(self.path)

        return self._cnf

    def check(self):
        return isfile(self.path)

    def values(self, solution):
        return {}

    @staticmethod
    def has_values():
        return False


class Cipher(Instance):
    tag = None
    path = None
    name = 'Cipher'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_stream = kwargs['key_stream']

    def values(self, solution):
        return {
            'key_stream': self.key_stream.values(solution=solution)
        } if solution is not None else {}

    @staticmethod
    def has_values():
        return True


StreamCipher = Cipher


class BlockCipher(Cipher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.public_key = kwargs['public_key']

    def values(self, solution):
        return {
            'public_key': self.public_key.values(solution=solution),
            'key_stream': self.key_stream.values(solution=solution)
        } if solution is not None else {}


__all__ = [
    'Cipher',
    'Instance',
    'SecretKey',
    'PublicKey',
    'KeyStream',
    'BlockCipher',
    'StreamCipher'
]
