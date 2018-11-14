import numpy as np


def gen_population(args):
    chromosome_length = len(args['dataset'])
    pop_size = args['pop_size']
    initialize_method = args['initialize_method']
    chromosome_range = range(chromosome_length)
    pop = []

    if (initialize_method == 'random'):
        for i in range(pop_size):
            pop.append(np.random.permutation(chromosome_range))

    args['population'] = pop
