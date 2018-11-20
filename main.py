#!/usr/bin/env python3


from src import evaluate, offspring_generation, select
from src.utility import *


def main():
    """ Entry point of program """

    # check command line args
    check_args()

    args = {
        'datafile': sys.argv[1],
        'pop_size': 20,
        'initialize_method': 'random',
        'parent_selection': 'random',
        'recombination': 'cut_crossfill',
        'crossover_rate': 0.9,
        'survivor_selection': 'mu_plus_lambda',
        'mutation_rate': 0.2,
        'generations': 1000,
        'box_cutting_points_n': 40,
        'knn_k': 40
    }


    args['initialize_method'] = 'kmeans'
    args['recombination'] = 'best_order'

    print_banner(args)

    # print performance metrics
    print_performance_metrics(args)

    # print population stats
    evaluate.print_stats(args)

    # process every generation
    for i in range(args['generations']):
        print("Generation %d: " % i)
        evaluate.eval_population(args)
        select.parents(args)
        offspring_generation.recombination(args)
        offspring_generation.mutation(args)
        evaluate.eval_offspring(args)
        select.survivors(args)
        evaluate.print_stats(args)

    evaluate.print_final(args)


# run main
if __name__ == "__main__":
    main()
