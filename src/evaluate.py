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

    # not our actual fitness function
    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]
        individual_sum += distance_matrix[population[individual_idx][0]][population[individual_idx][1]]

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
    population = args['population']
    dataset = args['dataset']

    print("The best individual: ")
    for j in range(1):
        print("#%d (fitness: %d): %s" % (j, args['fitness'][x[j]], args['population'][x[j]]))

        # UNCOMMENT TO SEE THE BEST 5 GRAPHICALLY
        x1, y = [], []
        # print fitness of best individuals
        for i in range(len(population[x[j]])):
            x1.append(dataset[population[x[j]][i]][0])
            y.append(-dataset[population[x[j]][i]][1])
            # add the first city to connect to the last
        x1.append(dataset[population[x[j]][0]][0])
        y.append(-dataset[population[x[j]][0]][1])

        plt.plot(y, x1, '-o')
        plt.show()

    pass


def eval_offspring(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'offspring_fitness' to the dictionary
    """
    # TODO: This is a repeat of the above. Combine them somehow

    population = args['offspring']
    distance_matrix = args['distance_matrix']

    fitness = []

    # not our actual fitness function
    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]

        fitness.append(-individual_sum)

    args['offspring_fitness'] = fitness
