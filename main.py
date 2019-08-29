import configuration as cfg

limit = cfg.to_seconds('24:00:00')

algorithm = cfg.Algorithm('evolution') \
    .comparator('max_min') \
    .condition(key='time', stop=lambda x: x > limit) \
    .strategy('plus', mu=1, lmbda=1) \
    .mutation('uniform', scale=1.) \
    .crossover('uniform', p=0.2) \
    .build()

cell = cfg.Cell('a5_1') \
    .logger() \
    .debugger(verb=3, size=5) \
    .build()

output = cfg.Output(**cell.output())

cell.close()
