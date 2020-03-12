from ..instance import *


class A5_1(StreamCipher):
    tag = 'a5_1'
    name = 'Cipher: A5/1'
    path = './templates/A5_1.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(8298, 128)
        )


__all__ = [
    'A5_1'
]
