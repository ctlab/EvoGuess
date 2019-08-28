from ..key_generator import StreamCipher


class ASG_96_112(StreamCipher):
    key_stream_start = 6547
    key_stream_len = 112

    secret_key_start = 1
    secret_key_len = 96

    name = "ASG_96_112"
    tag = "asg_96_112"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_asg = ASG_96_112(self.cnf)
        copy_asg.substitutions = self.substitutions

        return copy_asg
