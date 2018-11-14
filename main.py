#!/usr/bin/env python3
import os
import sys
import time

import src.data_import as data_import
import src.evaluate as evaluate
import src.initialize as initialize
import src.offspring_generation as offspring_generation
import src.select as select


def main():
    """ Entry point of program """

    # get parameters, dump into a dictionary
    args = parse_args()

    # read the data file
    with CodeTimer('read datafile'):
        data_import.parse_datafile(args)

    # calculate the distance matrix
    with CodeTimer('calculate distance matrix'):
        data_import.calc_distance_matrix(args)

    # generate a starter population
    with CodeTimer('generate starter population'):
        initialize.gen_population(args)

    # give an idea of evaluation function performance
    with CodeTimer('initial eval time'):
        evaluate.eval_population(args)

    with CodeTimer('parent selection'):
        select.parents(args)

    with CodeTimer('recombination'):
        offspring_generation.recombination(args)

    with CodeTimer('mutation'):
        offspring_generation.mutation(args)

    with CodeTimer('offspring_fitness'):
        evaluate.eval_offspring(args)

    with CodeTimer('survivor selection'):
        select.survivors(args)

    evaluate.print_stats(args)

    for i in range(0, args['generations']):
        print("Generation %d: " % i)
        evaluate.eval_population(args)
        select.parents(args)
        offspring_generation.recombination(args)
        offspring_generation.mutation(args)
        evaluate.eval_offspring(args)
        select.survivors(args)
        evaluate.print_stats(args)

    evaluate.print_final(args)


def parse_args():
    """ Read the command line and generate an object that encompasses all parameters

    :return: A dictionary that is used as a global dictionary between functions
    """

    # TODO: parse everything from command line? maybe not necessary
    print("EA-TSP by E Garg, S Parson, T Rahman, J Wagner")
    if len(sys.argv) != 2:
        die("Wrong number of parameters")

    if not os.path.isfile(sys.argv[1]):
        die("File '" + str(sys.argv[1]) + "' does not exist.")

    args = {
        'datafile': sys.argv[1],
        'pop_size': 4663,
        'initialize_method': 'random',
        'parent_selection': 'random',
        'recombination': 'cut_crossfill',
        'crossover_rate': 0.9,
        'survivor_selection': 'mu_plus_lambda',
        'mutation_rate': 1,
        'generations': 1000,
    }

    print_banner(args)
    return args


def print_banner(arguments):
    """ Output some details about this program

    :param arguments: The global parameter dictionary
    :return:
    """

    print("\nRuntime parameters:")
    for k, v in sorted(arguments.items()):
        print("\t'%s': %s" % (str(k), str(v)))
    print()


def die(error):
    """ Helper function to die on error

    :param error: Error message to display to user
    :return: Kills the program
    """

    print("Error: " + error)
    print("Usage: python3.5 " + str(sys.argv[0]) +
          " datafile")
    raise SystemExit


# CodeTimer derived from
# https://stackoverflow.com/questions/14452145/how-to-measure-time-taken-between-lines-of-code-in-python
# used to time each block, for profiling purposes
class CodeTimer:
    def __init__(self, name=None):
        self.name = "'" + name + "'" if name else ''

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (time.perf_counter() - self.start) * 1000.0
        print("%s: %.2f ms" % (self.name, self.took))


# run main
if __name__ == "__main__":
    main()
