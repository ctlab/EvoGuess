from ..key_generator import StreamCipher


class A5_1(StreamCipher):
    key_stream_start = 8298
    key_stream_len = 128

    secret_key_start = 1
    secret_key_len = 64

    name = "A5/1"
    tag = "a5_1"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_a5_1 = A5_1(self.cnf)
        copy_a5_1.substitutions = self.substitutions

        return copy_a5_1
