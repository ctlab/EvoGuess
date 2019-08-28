from predictor.method.impl.gad import GuessAndDetermine
from predictor.method.impl.ibs import InverseBackdoorSets

methods = {
    'ibs': InverseBackdoorSets,
    'gad': GuessAndDetermine
}


def get_method(options):
    return methods[options['name']](**options)
