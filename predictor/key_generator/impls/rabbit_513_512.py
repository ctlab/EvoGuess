from ..key_generator import StreamCipher


class Rabbit_513_512(StreamCipher):
    key_stream_start = 97938
    key_stream_len = 512

    secret_key_start = 1
    secret_key_len = 513

    name = "Rabbit_513_512"
    tag = "rabbit_513_512"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_rabbit = Rabbit_513_512(self.cnf)
        copy_rabbit.substitutions = self.substitutions

        return copy_rabbit
