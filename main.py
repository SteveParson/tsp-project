#!/usr/bin/env python3

from src import evaluate, offspring_generation, select
from src.utility import *


def main():
    """ Entry point of program """

    # check command line args
    args = {}

    ####################################################
    # COMMENT THIS SECTION OUT TO LOAD ARGS FROM A FILE
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
        'kca_k': 40
    }
    args['initialize_method'] = 'kmeans'
    args['recombination'] = 'best_order'
    ####################################################

    # see if we have an argument file specified
    args2 = check_args()

    # if so, use it
    if args2:
        args = args2

    # otherwise, dump our args to a .json file in the current directory
    else:
        args['argfile'] = str(hash(frozenset(args.items()))) + ".json"
        with open(args['argfile'], "w") as f:
            json.dump(args, f, indent=1)

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
