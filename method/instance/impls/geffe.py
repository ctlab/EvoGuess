from ..instance import *


class Geffe(StreamCipher):
    tag = 'geffe'
    name = 'Cipher: Geffe'
    path = './templates/Geffe.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(301, 100)
        )


__all__ = [
    'Geffe'
]
