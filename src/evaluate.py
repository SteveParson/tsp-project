import csv

import matplotlib.pyplot as plt

from .utility import *


def eval_population(args):
    """
    Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'fitness' to the dictionary
    """

    population = args['population']
    distance_matrix = args['distance_matrix']

    fitness = []

    # For every individual in the population
    for individual_idx in range(len(population)):

        individual_sum = 0

        # Point at the individual
        individual = population[individual_idx]

        # Look at every city pair
        for allele_idx in range(len(individual) - 1):
            city1 = individual[allele_idx]
            city2 = individual[allele_idx + 1]

            # Add their distance to the total
            individual_sum += distance_matrix[city1][city2]

        # Add the distance from the last node, back to the starting node
        individual_sum += distance_matrix[individual[0]][individual[-1]]

        # Add this individual's sum to the list of fitnesses, as a negative
        # value, so that we view this as a maximization problem
        fitness.append(-individual_sum)

    args['fitness'] = fitness


def print_stats(args, export, export_fp):
    """
    Print statistics about a current generation

    :param args:
    :param export:
    :param export_fp:
    :return:
    """
    fitness = args['fitness']
    args['max'] = -np.max(fitness)
    args['mean'] = -np.mean(fitness)
    args['sd'] = np.std(fitness)
    print("Max: %d\tMean: %d\tSD: %d" % (args['max'], args['mean'], args['sd']))

    # Write the the output to a CSV file, if specified.
    if export:
        with open(export_fp, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([args['max'], args['mean'], args['sd']])


def plot(args):
    """
    Wrapper function to call the plotter.

    :param args: The global parameter dictionary
    :return:
    """
    args['plotter'].plot()


def print_final(args, visualize=False):
    """
    Print the final fitness values

    :param args: The global parameter dictionary
    :param visualize: A boolean value, which indicates whether or not visualization is currently in use.
    :return:
    """
    distribution = rankify(args['fitness'])
    print("The best individual: ")
    print("#%d (fitness: %d): %s" % (0, -args['fitness'][distribution[0]], args['population'][distribution[0]]))

    # TODO: Change this check to look for args['plotter'] instead, so that we
    # TODO: can loose the parameter in the method
    # We need to halt the program so that the user can examine the plots
    if visualize: input()


# TODO: Merge the function with the other one
def eval_offspring(args):
    population = args['offspring']
    distance_matrix = args['distance_matrix']

    fitness = []

    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]
        individual_sum += distance_matrix[population[individual_idx][0]][population[individual_idx][-1]]

        fitness.append(-individual_sum)

    args['offspring_fitness'] = fitness
