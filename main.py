#!/usr/bin/env python3

from src import initialize, evaluate, offspring_generation, select, data_import
from src.utility import *


def main():
    args = check_args()

    print("EA-TSP by E Garg, S Parson, T Rahman, J Wagner")

    print_config(args)

    if args['performance_debug']:
        print_performance_metrics(args)
        evaluate.print_stats(args)

    data_import.parse_datafile(args)
    data_import.calc_distance_matrix(args)
    initialize.gen_population(args)

    for i in range(args['generations']):
        print("Generation %d: " % i, end="")
        evaluate.eval_population(args)
        select.parents(args)
        offspring_generation.recombination(args)
        offspring_generation.mutation(args)
        evaluate.eval_offspring(args)
        select.survivors(args)
        evaluate.print_stats(args)

    evaluate.print_final(args)


if __name__ == "__main__":
    main()
