from ..cipher import *


class Mickey(StreamCipher):
    tag = 'mickey'
    name = 'Cipher: Mickey'
    path = './templates/Mickey.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 200),
            key_stream=KeyStream(71829, 250)
        )


__all__ = [
    'Mickey'
]
