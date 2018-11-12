import numpy as np


def gen_population(args):
    pop = []
    chromosome_length = len(args['dataset'])
    chromosome_range = range(chromosome_length)

    if (args['initialize_method'] == 'random'):
        for i in range(0, args['pop_size']):
            pop.append(np.random.permutation(chromosome_range))

    args['population'] = pop
