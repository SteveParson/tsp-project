
import matplotlib.pyplot as plt

from .utility import *


def eval_population(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'fitness' to the dictionary
    """

    population = args['population']
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

    args['fitness'] = fitness


def print_stats(args):
    fitness = args['fitness']
    args['max'] = -np.max(fitness)
    args['mean'] = -np.mean(fitness)
    args['sd'] = np.std(fitness)
    print("%d %d %d" % (args['max'], args['mean'], args['sd']))


def plot(args):
    args['plotter'].plot()

def print_final(args):
    x = rankify(args['fitness'])
    print("The best individual: ")
    print("#%d (fitness: %d): %s" % (0, -args['fitness'][x[0]], args['population'][x[0]]))
    input()

def eval_offspring(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'offspring_fitness' to the dictionary
    """

    population = args['offspring']
    distance_matrix = args['distance_matrix']

    fitness = []

    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]

        fitness.append(-individual_sum)

    args['offspring_fitness'] = fitness
