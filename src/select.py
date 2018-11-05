import numpy as np


def parents(args):
    # random selection for testing purposes
    pop_size = args['pop_size']
    mp_size = args.get('mating_pool_size', int(pop_size / 2))

    # even number of mates
    mp_size = mp_size + 1 if (mp_size % 2 == 1) else mp_size

    args['mating_pool'] = np.random.choice(range(pop_size), size=mp_size, replace=False)


def survivors(args):
    pass