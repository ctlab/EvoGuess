from ..key_generator import StreamCipher


class Grain_v0(StreamCipher):
    key_stream_start = 1306
    key_stream_len = 160

    secret_key_start = 1
    secret_key_len = 160

    name = "Grain ver 0"
    tag = "grain_v0"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_grain = Grain_v0(self.cnf)
        copy_grain.substitutions = self.substitutions

        return copy_grain
