from ..cipher import *


class ASG_72_76(StreamCipher):
    tag = 'asg_72_76'
    name = 'Cipher: ASG 72/76'
    path = './templates/ASG_72_76.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 72),
            key_stream=KeyStream(3351, 76)
        )


class ASG_96_112(StreamCipher):
    tag = 'asg_96_112'
    name = 'Cipher: ASG 96/112'
    path = './templates/ASG_96_112.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 96),
            key_stream=KeyStream(6547, 112)
        )


class ASG_192_200(StreamCipher):
    tag = 'asg_192_200'
    name = 'Cipher: ASG 192/200'
    path = './templates/ASG_192_200.cnf'

    def __init__(self):
        super().__init__(
            secret_key=SecretKey(1, 192),
            key_stream=KeyStream(22506, 200)
        )


__all__ = [
    'ASG_72_76',
    'ASG_96_112',
    'ASG_192_200'
]
