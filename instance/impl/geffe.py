from ..instance import *


class Geffe(StreamCipher):
    tag = 'geffe'
    name = 'Cipher: Geffe'

    def __init__(self):
        self.path = self.build_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(301, 100)
        )


__all__ = [
    'Geffe'
]
