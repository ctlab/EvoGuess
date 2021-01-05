from ..instance import *


class Salsa20(StreamCipher):
    base = 2
    tag = 'salsa20'
    name = 'Cipher: Salsa 20'

    def __init__(self):
        self.cnf_path = self.build_cnf_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 512),
            key_stream=KeyStream(26465, 512)
        )


__all__ = [
    'Salsa20'
]
