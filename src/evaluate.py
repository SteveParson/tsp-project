def eval_population(args):
    """ Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'fitness' to the dictionary
    """

    fitness = []
    population = args['population']

    # not our actual fitness function
    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx])):
            individual_sum += population[individual_idx][allele_idx]

        fitness.append(individual_sum)

    args['fitness'] = fitness
