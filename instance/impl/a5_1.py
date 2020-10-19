from ..instance import *


class A5_1(StreamCipher):
    tag = 'a5_1'
    name = 'Cipher: A5/1'

    def __init__(self):
        self.path = self.build_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(8298, 128)
        )


__all__ = [
    'A5_1'
]