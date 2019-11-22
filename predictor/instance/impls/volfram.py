from ..instance import *


class Volfram(StreamCipher):
    tag = 'volfram'
    name = 'Volfram'
    path = './templates/Volfram.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 128),
            key_stream=KeyStream(12417, 128)
        )


__all__ = [
    'Volfram'
]
