from ..cipher import *


class Salsa20(StreamCipher):
    tag = "salsa20"
    name = "Cipher: Salsa 20"
    path = './templates/Salsa20.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 512),
            key_stream=KeyStream(26465, 512)
        )


__all__ = [
    'Salsa20'
]
