from .impls.a5_1 import A5_1
from .impls.e0 import E0
from .impls.mickey import Mickey
from .impls.salsa20 import Salsa20
from .impls.rabbit_513_512 import Rabbit_513_512

from .impls.bivium import Bivium
from .impls.trivium import Trivium
from .impls.trivium_64 import Trivium_64
from .impls.trivium_96 import Trivium_96

from .impls.grain_v0 import Grain_v0
from .impls.grain_v1 import Grain_v1

from .impls.present_5_2kp import Present_5_2KP
from .impls.present_6_1kp import Present_6_1KP
from .impls.present_6_2kp import Present_6_2KP

from .impls.asg_72_76 import ASG_72_76
from .impls.asg_96_112 import ASG_96_112
from .impls.asg_192_200 import ASG_192_200

from .impls.geffe import Geffe
from .impls.volfram import Volfram

key_generators = {
    "a5_1": A5_1,
    "e0": E0,
    "mickey": Mickey,
    "salsa20": Salsa20,
    "rabbit_513_512": Rabbit_513_512,
    # Trivium
    "bivium": Bivium,
    "trivium": Trivium,
    "trivium_64": Trivium_64,
    "trivium_96": Trivium_96,
    # Grain
    "grain_v0": Grain_v0,
    "grain_v1": Grain_v1,
    # Present
    "present_5_2kp": Present_5_2KP,
    "present_6_1kp": Present_6_1KP,
    "present_6_2kp": Present_6_2KP,
    # ASG
    "asg_72_76": ASG_72_76,
    "asg_96_112": ASG_96_112,
    "asg_192_200": ASG_192_200,
    # Other
    "geffe": Geffe,
    "volfram": Volfram,
}


def get_algorithm(tag):
    return key_generators[tag]
