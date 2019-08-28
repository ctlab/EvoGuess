from ..key_generator import BlockCipher


class Present_5_2KP(BlockCipher):
    key_stream_start = 1825
    key_stream_len = 128

    secret_key_start = 1
    secret_key_len = 80

    public_key_start = 81
    public_key_len = 128

    name = "Present_5_2KP"
    tag = "present_5_2kp"

    def __init__(self, cnf):
        BlockCipher.__init__(self, cnf)

    def __copy__(self):
        copy_present = Present_5_2KP(self.cnf)
        copy_present.substitutions = self.substitutions

        return copy_present
