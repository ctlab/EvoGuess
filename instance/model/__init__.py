from .interval import *
from .backdoor import *

SecretKey = Interval
PublicKey = Interval
KeyStream = Interval

__all__ = [
    'Backdoor',
    'SecretKey',
    'PublicKey',
    'KeyStream',
]
