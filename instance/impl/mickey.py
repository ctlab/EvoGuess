from ..instance import *


class Mickey(StreamCipher):
    tag = 'mickey'
    name = 'Cipher: Mickey'

    def __init__(self):
        self.path = self.build_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 200),
            key_stream=KeyStream(71829, 250)
        )


__all__ = [
    'Mickey'
]
