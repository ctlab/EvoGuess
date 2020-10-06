from ..instance import *


class Volfram(StreamCipher):
    tag = 'volfram'
    name = 'Cipher: Volfram'

    def __init__(self):
        self.path = self.build_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 128),
            key_stream=KeyStream(12417, 128)
        )


__all__ = [
    'Volfram'
]
