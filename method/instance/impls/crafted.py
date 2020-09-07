from ..instance import *

params = {
    'eulcbip': ('eulcbip-8-UNSAT.sat05-3937.reshuffled-07', 400),
    'pmg': ('pmg-13-UNSAT.sat05-3941.reshuffled-07', 409),
    'clqcolor': ('unsat-set-a-clqcolor-16-10-11.sat05-1253.reshuffled-07', 456),
    'challenge': ('challenge-105', 105),
    'mod': ('mod4block_2vars_9gates_u2_autoenc', 430),
}


class Crafted(Instance):
    tag = 'crafted'

    def __init__(self, key):
        self.name = 'Instance: Crafted (%s)' % params[key][0]
        self.path = './templates/Crafted/%s.cnf' % params[key][0]
        super().__init__(secret_key=SecretKey(1, params[key][1]))


class SGEN(Instance):
    tag = 'sgen'

    def __init__(self, v, n, seed='5-1'):
        self.name = 'Instance: SGEN%d-%d (seed: %s)' % (v, v * n, seed)
        if v == 6:
            self.path = './templates/Crafted/sgen%d-%d-%s.cnf' % (v, v * n, seed)
            super().__init__(secret_key=SecretKey(1, n))
        else:
            self.path = None


__all__ = [
    'SGEN',
    'Crafted'
]
