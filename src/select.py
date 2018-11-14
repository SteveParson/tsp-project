from .utility import *


def parents(args):
    """ Selects parents to form a mating pool

    :param args: The global parameter dictionary
    :return: Adds the mating_pool indices to the dictionary
    """
    # random selection for testing purposes
    pop_size = args['pop_size']

    # use mp_size if availab,e otherwise set it to half of the population size
    # this default selection and assignment should happen somewhere else
    mp_size = args.get('mp_size', int(pop_size / 2))
    args['mp_size'] = mp_size

    # even number of mates
    mp_size = mp_size + 1 if (mp_size % 2 == 1) else mp_size

    if args['parent_selection'] == 'random':
        args['mating_pool'] = random_selection(range(pop_size), mp_size, False)


def survivors(args):
    """ Selects survivors in the population

    :param args: Our global dictionary
    :return: Reassigns 'population' and 'fitness' in the dictionary
    """

    survivor_selection = args['survivor_selection']

    if survivor_selection == 'mu_plus_lambda':
        # pool the population and offspring
        full_population = args['population'] + args['offspring']
        full_fitness = args['fitness'] + args['offspring_fitness']
        mu = args['pop_size']

        # rank their fitnesses, keep only mu
        rank_vector = rankify(full_fitness)[:mu]

        # keep only the top mu individuals
        population, fitness = [], []

        for index in rank_vector:
            population.append(full_population[index])
            fitness.append(full_fitness[index])

        # reassign the dictionary
        args['population'] = population
        args['fitness'] = fitness
        return

    # TODO: use numpy to do this
    if survivor_selection == 'random':
        full_population = args['population'] + args['offspring']
        full_fitness = args['fitness'] + args['offspring_fitness']
        full_pool = len(full_population)
        mu = args['pop_size']

        # get a random selection
        choices = random_selection(range(full_pool), mu, False)
        population, fitness = [], []

        # make the choices
        for index in choices:
            population.append(full_population[index])
            fitness.append(full_fitness[index])

        # reassign the dictionary
        args['population'] = population
        args['fitness'] = fitness
    return


def random_selection(individuals, number_to_choose, with_replace=False):
    """ Returns a random sample from a set, with or without replacement

    :param individuals: The choices
    :param number_to_choose: How many to choose
    :param with_replace: Pick with replacement? (Default: False)
    :return: The random sample
    """
    return np.random.choice(individuals, size=number_to_choose, replace=with_replace)
