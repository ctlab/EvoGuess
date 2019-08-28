from ..key_generator import StreamCipher


class ASG_72_76(StreamCipher):
    key_stream_start = 3351
    key_stream_len = 76

    secret_key_start = 1
    secret_key_len = 72

    name = "ASG_72_76"
    tag = "asg_72_76"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_asg = ASG_72_76(self.cnf)
        copy_asg.substitutions = self.substitutions

        return copy_asg
