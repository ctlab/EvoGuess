from ..instance import *


class Bivium(StreamCipher):
    tag = 'bivium'
    name = 'Bivium'
    path = './templates/Bivium.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 177),
            key_stream=KeyStream(443, 200)
        )


class Trivium_64(StreamCipher):
    tag = 'trivium_64'
    name = 'Cipher: Trivium 64/75'
    path = './templates/Trivium_64.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(398, 75)
        )


class Trivium_96(StreamCipher):
    tag = 'trivium_96'
    name = 'Cipher: Trivium 96'
    path = './templates/Trivium_96.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 96),
            key_stream=KeyStream(530, 100)
        )


class Trivium(StreamCipher):
    tag = 'trivium'
    name = 'Cipher: Trivium'
    path = './templates/Trivium.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 288),
            key_stream=KeyStream(1588, 300)
        )


__all__ = [
    'Bivium',
    'Trivium',
    'Trivium_64',
    'Trivium_96'
]
