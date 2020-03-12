from ..instance import *


class Rabbit_513_512(StreamCipher):
    tag = 'rabbit_513_512'
    name = 'Cipher: Rabbit 513/512'
    path = './templates/Rabbit_513_512.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 513),
            key_stream=KeyStream(97938, 512)
        )


__all__ = [
    'Rabbit_513_512'
]
