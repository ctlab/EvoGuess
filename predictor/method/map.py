from predictor.method.impls.gad import GuessAndDetermine
from predictor.method.impls.ibs import InverseBackdoorSets

methods = {
    'ibs': InverseBackdoorSets,
    'gad': GuessAndDetermine
}


def get_method(options):
    return methods[options['name']](**options)
