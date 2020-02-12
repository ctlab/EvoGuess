from .models import var, cnf

from .impls.e0 import *
from .impls.a5_1 import *

from .impls.asg import *
from .impls.grain import *
from .impls.trivium import *
from .impls.present import *

from .impls.mickey import *
from .impls.rabbit import *
from .impls.salsa20 import *

from .impls.sorting import *

from .impls.md4 import *

from .impls.geffe import *
from .impls.volfram import *


def get(name):
    args = []
    if ':' in name:
        [name, args] = name.split(':')
        args = map(int, args.split('_'))
    return {
        'e0': E0,
        'a5': A5_1,
        # asg
        'asg72': ASG_72_76,
        'asg96': ASG_96_112,
        'asg192': ASG_192_200,
        # grain
        'gr0': Grain_v0,
        'gr1': Grain_v1,
        # trivium
        'tr': Trivium,
        'biv': Bivium,
        'tr64': Trivium_64,
        'tr96': Trivium_96,
        # present
        'pr5_2': Present_5_2KP,
        'pr6_1': Present_6_1KP,
        'pr6_2': Present_6_2KP,
        # sorting
        'bvi': BubbleVsInsert,
        'bvs': BubbleVsSelection,
        # hash
        'md4': MD4,
        # trash
        'geffe': Geffe,
        'volfram': Volfram
    }[name](*args)
