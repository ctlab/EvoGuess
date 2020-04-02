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
    path = './templates/Test/200-30-70.cnf'

    def __init__(self):
        super().__init__(secret_key=SecretKey(1, 70))


__all__ = [
    'Test_100_100',
    'Test_200_30_70'
]
