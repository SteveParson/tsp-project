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

        fitness.append(individual_sum)

    args['fitness'] = fitness


def print_stats():
    print("Not implemented")
