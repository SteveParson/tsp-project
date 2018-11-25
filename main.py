#!/usr/bin/env python3

from src import initialize, evaluate, offspring_generation, select, data_import
from src.utility import *
import multiprocessing as mp
import matplotlib.pyplot as plt




def main():
    args = check_args()
    # swap length is relative to the number of clusters
    args['swap_length'] = int(1 / args['kca_k'] * 3)

    print(args['swap_length'])

    print("EA-TSP by E Garg, S Parson, T Rahman, J Wagner")

    print_config(args)

    if args['performance_debug']:
        print_performance_metrics(args)
        evaluate.print_stats(args)

    data_import.parse_datafile(args)
    data_import.calc_distance_matrix(args)
    initialize.gen_population(args)
    initialize.create_plotter(args)

    for i in range(args['generations']):
        args['current_gen'] = i
        print("Generation %d: " % i, end="")
        evaluate.eval_population(args)
        select.parents(args)
        offspring_generation.recombination(args)
        offspring_generation.mutation(args)
        evaluate.eval_offspring(args)
        select.survivors(args)
        evaluate.print_stats(args)
        evaluate.plot(args)

    evaluate.print_final(args)

if __name__ == "__main__":
    # If we're on MacOSX, praise Steve Jobs first
    if plt.get_backend() == "MacOSX":
        mp.set_start_method("forkserver")
    main()
