from .models import *
from .models.var import *


class Cipher:
    tag = None
    path = None
    name = 'Cipher'

    def __init__(self, **kwargs):
        self._cnf = None
        self.secret_key = kwargs['secret_key']
        self.key_stream = kwargs['key_stream']

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

    def resolve(self, solution):
        return {
            'secret_key': self.secret_key.values(solution=solution),
            'key_stream': self.key_stream.values(solution=solution)
        } if solution is not None else {}


StreamCipher = Cipher


class BlockCipher(Cipher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.public_key = kwargs['public_key']

    def resolve(self, solution):
        return {
            'secret_key': self.secret_key.values(solution=solution),
            'public_key': self.public_key.values(solution=solution),
            'key_stream': self.key_stream.values(solution=solution)
        } if solution is not None else {}


__all__ = [
    'Cipher',
    'SecretKey',
    'PublicKey',
    'KeyStream',
    'BlockCipher',
    'StreamCipher'
]
