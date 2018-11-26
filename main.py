#!/usr/bin/env python3

import csv

from src import initialize, evaluate, offspring_generation, \
    select, data_import
from src.utility import *
import multiprocessing as mp
import matplotlib.pyplot as plt


def main():
    cmd_args = parse_args()
    args = load_args_from_file(cmd_args.args_file)

    # swap length is relative to the number of clusters
    args['swap_length'] = 3

    print("EA-TSP by E Garg, S Parson, T Rahman, J Wagner")

    if cmd_args.visualize and cmd_args.test_runs > 1:
        print("WARNING: Can't plot real-time data for more than one test run!")
        cmd_args.visualize = False

    print_config(args)

    if cmd_args.debug:
        print_performance_metrics(args)
        evaluate.print_stats(args)

    data_import.parse_datafile(args)
    data_import.calc_distance_matrix(args)
    initialize.gen_population(args)

    if cmd_args.visualize:
        initialize.create_plotter(args)

    for run_num in range(cmd_args.test_runs):
        export_fp = "{}.{}.csv".format(cmd_args.args_file, run_num)
        if cmd_args.export:
            with open(export_fp, 'w') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(['max', 'mean', 'std dev'])

        for i in range(args['generations']):
            args['current_gen'] = i
            print("Generation %d: " % i, end="")
            evaluate.eval_population(args)
            select.parents(args)
            offspring_generation.recombination(args)
            offspring_generation.mutation(args)
            evaluate.eval_offspring(args)
            select.survivors(args)
            evaluate.print_stats(args, cmd_args.export, export_fp)

            if cmd_args.visualize:
                evaluate.plot(args)

        evaluate.print_final(args, cmd_args.visualize)

if __name__ == "__main__":
    # If we're on MacOSX, praise Steve Jobs first
    if plt.get_backend() == "MacOSX":
        mp.set_start_method("forkserver")
    main()
