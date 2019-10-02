from ..cipher import *


class Present_5_2KP(BlockCipher):
    tag = 'present_5_2kp'
    name = 'Cipher: Present 5/2KP'
    path = './templates/Present_5_2KP.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 80),
            public_key=PublicKey(81, 128),
            key_stream=KeyStream(1825, 128)
        )


class Present_6_1KP(BlockCipher):
    tag = 'present_6_1kp'
    name = 'Cipher: Present 6/1KP'
    path = './templates/Present_6_1KP.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 80),
            public_key=PublicKey(81, 80),
            key_stream=KeyStream(1185, 64)
        )


class Present_6_2KP(BlockCipher):
    tag = 'present_6_2kp'
    name = 'Cipher: Present 6/2KP'
    path = './templates/Present_6_2KP.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 80),
            public_key=PublicKey(81, 128),
            key_stream=KeyStream(2081, 128)
        )


__all__ = [
    'Present_5_2KP',
    'Present_6_1KP',
    'Present_6_2KP'
]
