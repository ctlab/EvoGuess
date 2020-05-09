from ..instance import *


class Test_100_100(Instance):
    tag = 'test_100_100'
    name = 'Instance: Test_100_100'
    path = './templates/Test/100_100.cnf'

    def __init__(self):
        super().__init__(secret_key=SecretKey(1, 100))


class Test_200_30_70(Instance):
    tag = 'test_200_30_70'
    name = 'Instance: Test_200_30_70'
    path = './templates/Test/200_30_70.cnf'

    def __init__(self):
        super().__init__(secret_key=SecretKey(1, 70))


class DFA_200_399_150(Instance):
    tag = 'dfa_200_399_150'

    name = 'Instance: DFA_200_399_150'
    path = './templates/Test/dfa-equivalence_cycle_200_399_150.cnf'

    def __init__(self):
        super().__init__(secret_key=SecretKey(1, 150))


__all__ = [
    'Test_100_100',
    'Test_200_30_70',
    'DFA_200_399_150'
]
