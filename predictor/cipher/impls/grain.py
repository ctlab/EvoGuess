from ..cipher import *


class Grain_v0(StreamCipher):
    tag = 'grain_v0'
    name = 'Cipher: Grain v0'
    path = './templates/Grain_v0.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 160),
            key_stream=KeyStream(1306, 160)
        )


class Grain_v1(StreamCipher):
    tag = 'grain_v1'
    name = 'Cipher: Grain v1'
    path = './templates/Grain_v1.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 160),
            key_stream=KeyStream(1786, 160)
        )


__all__ = [
    'Grain_v0',
    'Grain_v1'
]
