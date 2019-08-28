from ..key_generator import StreamCipher


class Mickey(StreamCipher):
    key_stream_start = 71829
    key_stream_len = 250

    secret_key_start = 1
    secret_key_len = 200

    name = "Mickey"
    tag = "mickey"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_mickey = Mickey(self.cnf)
        copy_mickey.substitutions = self.substitutions

        return copy_mickey
