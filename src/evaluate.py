import numpy as np


def eval_population(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'fitness' to the dictionary
    """

    fitness = []
    population = args['population']
    distance_matrix = args['distance_matrix']

    # not our actual fitness function
    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]

        fitness.append(-individual_sum)

    args['fitness'] = fitness


def print_stats(args):
    fitness = args['fitness']
    print("  max, mean, std: %d %d %d" % (
        np.max(fitness),
        np.mean(fitness),
        np.std(fitness)))


def print_final(args):
    x = rankify(args['fitness'])
    print("The best 5 individuals: ")
    for i in range(5):
        print("#%d (fitness: %d)" % (i, args['fitness'][x[i]]))

    pass


def rankify(values):
    """ Rank an array

    :param values: An array of values
    :return: A ranking for the array of values
    """
    # TODO: This is also in another file. Maybe we should just use np.argsort directly, or make a utility function file
    return list(np.argsort(np.array(values)))[::-1]


def eval_offspring(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'offspring_fitness' to the dictionary
    """
    # TODO: This is a repeat of the above. Combine them somehow

    fitness = []
    population = args['offspring']
    distance_matrix = args['distance_matrix']

    # not our actual fitness function
    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]

        fitness.append(-individual_sum)

    args['offspring_fitness'] = fitness
