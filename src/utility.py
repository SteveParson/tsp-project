import json
import os
import sys
import time

import numpy as np


# CodeTimer derived from
# https://stackoverflow.com/questions/14452145/how-to-measure-time-taken-between-lines-of-code-in-python
# used to time each block, for profiling purposes

def order_subset_from_full_set(subset, full_set):
    """ Arranges a subset in an order defined by another set

    :param subset: A list containing the elements we wish to order
    :param full_set: A superset of subset, from which we wish to extract order information
    :return: subset, with the order from full_set
    """
    new_order = []

    for element in full_set:
        if element in subset:
            new_order.append(element)

    return new_order


def check_args():
    """
    This function gets the required arguments for the EA from a JSON
    file and returns it as a dictionary.
    """

    if len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            die("File '" + str(sys.argv[1]) + "' does not exist.")

        with open(sys.argv[2], 'r') as f:
            args = json.load(f)
    else:
        print("No argument file specified, using default...")
        with open('default_args.json', 'r') as f:
            args = json.load(f)

    return args

def print_performance_metrics(args):
    # read the data file
    with CodeTimer('read datafile'):
        from src import data_import
        data_import.parse_datafile(args)

    # calculate the distance matrix
    with CodeTimer('calculate distance matrix'):
        data_import.calc_distance_matrix(args)

    # generate a starter population
    with CodeTimer('generate starter population'):
        from src import initialize
        initialize.gen_population(args)

    # give an idea of evaluation function performance
    with CodeTimer('initial eval time'):
        from src import evaluate
        evaluate.eval_population(args)

    with CodeTimer('parent selection'):
        from src import select
        select.parents(args)

    with CodeTimer('recombination'):
        from src import offspring_generation
        offspring_generation.recombination(args)

    with CodeTimer('mutation'):
        offspring_generation.mutation(args)

    with CodeTimer('offspring_fitness'):
        evaluate.eval_offspring(args)

    with CodeTimer('survivor selection'):
        select.survivors(args)


def print_banner(args):
    """ Output some details about this program

    :param args: The global parameter dictionary
    :return:
    """

    print("\nRuntime parameters:")
    for k, v in sorted(args.items()):
        print("\t'%s': %s" % (str(k), str(v)))
    print()


def rankify(values):
    """ Rank an array

    :param values: An array of values
    :return: A ranking for the array of values
    """
    return list(np.argsort(np.array(values)))[::-1]


def die(error):
    """ Helper function to die on error

    :param error: Error message to display to user
    :return: Kills the program
    """

    print("Error: " + error)
    print("Usage: python3.5 " + str(sys.argv[0]) +
          " datafile args-file-json")
    raise SystemExit


class CodeTimer:
    def __init__(self, name=None):
        self.name = "'" + name + "'" if name else ''

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (time.perf_counter() - self.start) * 1000.0
        # print("%s: %.2f ms" % (self.name, self.took))
