from ..instance import *


class E0(StreamCipher):
    tag = 'e0'
    name = 'Cipher: E0'
    path = './templates/E0.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 128),
            key_stream=KeyStream(1785, 128)
        )


__all__ = [
    'E0'
]
