from predictor.concurrency.limit_pool import LimitPool

concurrency = {
    'ibs': LimitPool,
    'gad': LimitPool
}


def get_concurrency(options):
    return concurrency[options['name']](**options)
