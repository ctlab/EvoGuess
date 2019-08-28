from ..key_generator import StreamCipher


class A5_toy(StreamCipher):
    key_stream_start = 3931
    key_stream_len = 80

    secret_key_start = 1
    secret_key_len = 48

    name = "A5/1 48"
    tag = "a5_1_48"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_a5_toy = A5_toy(self.cnf)
        copy_a5_toy.substitutions = self.substitutions

        return copy_a5_toy
