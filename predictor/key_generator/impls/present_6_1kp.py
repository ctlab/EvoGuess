from ..key_generator import BlockCipher


class Present_6_1KP(BlockCipher):
    key_stream_start = 1185
    key_stream_len = 64

    secret_key_start = 1
    secret_key_len = 80

    public_key_start = 81
    public_key_len = 64

    name = "Present_6_1KP"
    tag = "present_6_1kp"

    def __init__(self, cnf):
        BlockCipher.__init__(self, cnf)

    def __copy__(self):
        copy_present = Present_6_1KP(self.cnf)
        copy_present.substitutions = self.substitutions

        return copy_present
