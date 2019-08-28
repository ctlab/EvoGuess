from functools import partial

from predictor.util.const import cnfs
from predictor.structure.cnf import Cnf, CnfSubstitution as CnfSub
from predictor.structure.backdoor import SecretKey
from predictor.util.environment import environment as env
from predictor.structure.interval import KeyStream, PublicKey


def get_f(algorithm, substitutions):
    return partial(CaseGenerator.get, algorithm, substitutions)


class CaseGenerator:
    def __init__(self, **kwargs):
        self.random_state = kwargs['rs']

        self.secret_key = SecretKey(env.algorithm)
        self.key_stream = KeyStream(env.algorithm)
        self.public_key = PublicKey(env.algorithm) if hasattr(env.algorithm, 'public_key_len') else None

    def get_init(self):
        substitutions = {'secret_key': CnfSub(*self.secret_key.values(rs=self.random_state))}
        if self.public_key is not None:
            substitutions['public_key'] = CnfSub(*self.public_key.values(rs=self.random_state))

        return get_f(env.algorithm, substitutions)

    def get_main(self, backdoor, solution, rnd=''):
        substitutions = {
            'key_stream': self.__substitution(self.key_stream, 's', solution, rnd),
            'backdoor': self.__substitution(backdoor, 'b', solution, rnd)
        }
        if self.public_key is not None:
            substitutions['public_key'] = self.__substitution(self.public_key, 'p', solution, rnd)

        return get_f(env.algorithm, substitutions)

    def __substitution(self, o, c, solution, rnd):
        return CnfSub(*o.values(**{'rs': self.random_state} if c in rnd else {'solution': solution}))

    @staticmethod
    def get(algorithm, substitutions):
        cnf = CaseGenerator.__cnf(algorithm)
        return algorithm(cnf).substitute(**substitutions)

    @staticmethod
    def __cnf(algorithm):
        if env.cnf is None:
            print('parsing cnf...')
            cnf_path = cnfs[algorithm.tag]
            env.cnf = Cnf.parse(cnf_path)

        return env.cnf
