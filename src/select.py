from .utility import *

import random


def parents(args):
    """
    Selects parents to form a mating pool.

    :param args: The global EA parameter dictionary.
    :return: Adds the mating_pool indices to the parameter dictionary.
    """

    if args['parent_selection'] == 'random':
        args['mating_pool'] = random_selection(range(args['pop_size']),
                                               args['mp_size'], False)

    if args['parent_selection'] == 'tournament_selection':
        parent_tournament_selection(args)

def parent_tournament_selection(args):
    """
    Selects parents using tournament selection.

    :param args: The global EA parameter dictionary.
    """
    selected_to_mate = []
    fitness = list(enumerate(args['fitness']))

    current_member = 0
    while current_member < args['mp_size']:
        random_individuals = random.sample(fitness, args['tournament_size'])
        best = max(random_individuals, key=lambda arr: arr[1])
        selected_to_mate.append(best[0])
        current_member = current_member + 1

    args['mating_pool'] = selected_to_mate

def survivors(args):
    """
    Selects survivors in the population.

    :param args: The global EA parameter dictionary.
    :return: Reassigns 'population' and 'fitness' in the dictionary
    """

    survivor_selection = args['survivor_selection']
    if survivor_selection == 'mu_plus_lambda':
        mu_plus_lambda_survivor_selection(args)

    if survivor_selection == 'random':
        random_survivor_selection(args)

def mu_plus_lambda_survivor_selection(args):
    """
    Select survivors using mu + lambda selection.

    :param args: The global EA parameter dictionary.
    """
    full_population = args['population'] + args['offspring']
    full_fitness = args['fitness'] + args['offspring_fitness']
    mu = args['pop_size']

    rank_vector = rankify(full_fitness)[:mu]
    population, fitness = [], []

    for index in rank_vector:
        population.append(full_population[index])
        fitness.append(full_fitness[index])

    args['population'] = population
    args['fitness'] = fitness

def random_survivor_selection(args):
    """
    Random survivor selection.

    :param args: The global EA parameter dictionary.
    """
    full_population = args['population'] + args['offspring']
    full_fitness = args['fitness'] + args['offspring_fitness']
    full_pool = len(full_population)
    mu = args['pop_size']

    choices = random_selection(range(full_pool), mu, False)
    population, fitness = [], []

    for index in choices:
        population.append(full_population[index])
        fitness.append(full_fitness[index])

    args['population'] = population
    args['fitness'] = fitness

def random_selection(individuals, number_to_choose, with_replace=False):
    """
    Returns a random sample from a set, with or without replacement

    :param individuals: The individuals to choose from.
    :param number_to_choose: The size of the sample.
    :param with_replace: Pick with replacement? (Default: False)
    :return: The random sample
    """
    return np.random.choice(individuals, size=number_to_choose, replace=with_replace)
