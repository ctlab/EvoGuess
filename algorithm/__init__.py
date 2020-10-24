from . import limit, evolution


def get_algorithm(params):
    return evolution.get_ea(params)


__all__ = [
    'limit',
    'evolution',
    'get_algorithm'
]
