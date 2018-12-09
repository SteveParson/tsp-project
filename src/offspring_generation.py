import random

from .utility import *
import multiprocessing as mp


def recombination(args):
    """
    Breed offspring from the mating pool

    :param args: The global parameter dictionary
    :return:
    """
    population = args['population']
    parents = args['mating_pool']
    mp_size = args['mp_size']
    crossover_rate = args['crossover_rate']
    recombination_type = args['recombination']
    fitness = args['fitness']

    parent_idx = 0
    number_of_children = 0
    results = []
    offspring = []

    while number_of_children < mp_size:
        parent1 = population[parents[parent_idx]]
        parent2 = population[parents[parent_idx + 1]]

        if random.random() < crossover_rate:
            if recombination_type == 'cut_crossfill':
                results.append(
                    cut_crossfill, args=(
                        np.array(parent1), np.array(parent2),
                    )
                )

            if recombination_type == 'best_order':
                n = args['box_cutting_points_n']
                chromosome_length = len(population[0])

                if not (2 <= n <= chromosome_length - 1):
                    die("box_cutting_points_n is out of range")

                best_individual = population[np.argmax(fitness)]
                results.append(
                    best_order(
                        chromosome_length, n, parent1, parent2, best_individual,
                    )
                )

        else:
            offspring.append(parent1.copy())
            offspring.append(parent2.copy())

        number_of_children += 2
        parent_idx = (parent_idx + 2) % mp_size

    for element in results:
        offspring.append(list(element[0]))
        offspring.append(list(element[1]))

    # Return the children
    args['offspring'] = offspring


def best_order(J, n, parent1, parent2, best_individual):
    """ Applies best-order crossover and produces two offspring
    using the order information from three parents.

    :param J: The length of our chromosome
    :param n: The number of cutting points for crossover
    :param parent1: Our first parent
    :param parent2: The second parent
    :param best_individual: The best individual in our population
    :return: Two offspring
    """
    np.random.seed()

    q = np.arange(n)
    q[-1] = J

    bad_cutting_point_sequence = True
    while bad_cutting_point_sequence:
        subarray = np.random.choice(np.arange(1, J), n - 2, replace=False)
        subarray.sort()
        q[1:n - 1] = subarray

        if len(q) != n:
            die("wrong size")
        # hypothesis: cutting point sequence is good
        bad_cutting_point_sequence = False

        # try to disprove the hypothesis at every cutting point
        for i in range(0, len(q) - 1):
            l_i = q[i + 1] - q[i]
            if not (0 <= l_i and l_i <= J // 3):
                bad_cutting_point_sequence = True

    # assign a parent for each sequence
    parent_choices = [random.randint(1, 3) for subsequence in range(n - 1)]


    offspring1 = np.zeros(J, dtype=int)
    offspring2 = np.zeros(J, dtype=int)

    for i in range(len(q) - 1):
        sp = q[i]
        ep = q[i + 1]

        if parent_choices[i] == 1:
            alleles1 = parent1[sp:ep]
            alleles2 = parent2[sp:ep]

        if parent_choices[i] == 2:
            alleles1 = order_subset_from_full_set(parent1[sp:ep], parent2)
            alleles2 = order_subset_from_full_set(parent2[sp:ep], parent1)

        if parent_choices[i] == 3:
            alleles1 = order_subset_from_full_set(parent1[sp:ep], best_individual)
            alleles2 = order_subset_from_full_set(parent2[sp:ep], best_individual)

        offspring1[sp:ep] = alleles1
        offspring2[sp:ep] = alleles2

    return offspring1, offspring2


def cut_crossfill(parent1, parent2):
    np.random.seed()
    chromosome_length = parent1.size
    crossover_point = np.random.randint(0, chromosome_length - 2)

    # Offspring 1
    crossover_idx = crossover_point + 1

    # Copy until the crossover point from parent1
    offspring1 = parent1.copy()
    offspring_idx = crossover_idx

    # Fill the other half of offspring until we have full coverage
    while offspring_idx != chromosome_length:

        # Grab an allele from parent2
        parent_allele = parent2[crossover_idx]

        # if it's not in offspring1, put it there
        if parent_allele not in offspring1[:offspring_idx]:
            offspring1[offspring_idx] = parent_allele
            offspring_idx += 1

        # increment and wrap around index pointer
        crossover_idx = (crossover_idx + 1) % chromosome_length

    # as above
    crossover_idx = crossover_point + 1
    offspring2 = parent2.copy()
    offspring_idx = crossover_idx
    while offspring_idx != chromosome_length:
        parent_allele = parent1[crossover_idx]
        if parent_allele not in offspring2[:offspring_idx]:
            offspring2[offspring_idx] = parent_allele
            offspring_idx += 1
        crossover_idx = (crossover_idx + 1) % chromosome_length

    return offspring1, offspring2


def mutation(args):
    mutation_rate = args['mutation_rate']
    mutation_func = MUTATION_FUNCTIONS[args['mutation']]
    offspring = args['offspring']

    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = mutation_func(offspring[i], length=args['swap_length'])


def permutation_swap(individual, length=-1):
    """
    Swaps two alleles randomly in a chromosome.

    :param individual: The chromosome
    :return: A mutated copy of the chromosome
    """
    # copy the individual
    mutant = individual.copy()

    # define mutation points
    point1, point2 = 0, 0

    # if the points are the same, generate two new numbers
    while point1 == point2:
        point1 = random.randint(0, len(mutant) - 1)
        point2 = random.randint(0, len(mutant) - 1)

    # swap the elements
    mutant[point1], mutant[point2] = mutant[point2], mutant[point1]
    return mutant


def insertion_mutation(individual, length=-1):
    """
    Inserts a random allele adjacent to another random allele
    in a given chromosome

    :param individual: The chromosome to mutate
    :param length: The size of the inversion
    :return: A mutated copy of the chromosome
    """
    positions = get_random_positions_based_on_cluster_size(individual, length)
    mutant = individual[:positions[0]] + individual[positions[0] + 1:positions[1] + 1]
    mutant.append(individual[positions[0]])
    mutant.extend(individual[positions[1] + 1:])
    return mutant


def inversion_swap(individual, length=-1):
    """
    Inverts a random subset of alleles in a given chromosome

    :param individual: The chromosome
    :param length: The size of the inversion
    :return: A mutated copy of the chromosome.
    """
    positions = get_random_positions_based_on_cluster_size(individual, length)
    seq = individual[positions[0]:positions[1] + 1]
    seq.reverse()
    return individual[:positions[0]] + seq + individual[positions[1] + 1:]


def two_opt_swap(individual, length=None):
    """
    Picks two adjacent pairs of alleles and swaps their respective elements.

    :param individual: The chromosome.
    :param length: Not used here, just for compatibility.
    :return: A mutated copy of the chromosome.
    """

    positions = get_random_positions_based_on_cluster_size(individual, 3)
    pair1 = [positions[0], positions[0] + 1]
    pair2 = [positions[-1] - 1, positions[-1]]
    seq1 = individual[pair1[0]:pair1[1] + 1]
    seq2 = individual[pair2[0]:pair2[1] + 1]
    seq1.reverse()
    seq2.reverse()
    return individual[:positions[0]] + seq1 + seq2 + individual[positions[1] + 1:]


def get_random_positions_based_on_cluster_size(individual, length):
    positions = [random.randint(0, len(individual) - 1)]
    if positions[0] + length >= len(individual):
        positions.append(positions[0] - length)
    else:
        positions.append(positions[0] + length)

    positions.sort()

    return positions


def cyclic(individual, length):
    mutation_funcs = [scramble, inversion_swap,
                      insertion_mutation, permutation_swap,
                      two_opt_swap]

    func = random.choice(mutation_funcs)

    return func(individual, length)


def scramble(individual, length=-1):
    """
    Scrambles a random subset of alleles in a given chromosome.

    :param individual: The chromosome
    :param length: The size of the inversion
    :return: A mutated copy of the chromosome.
    """
    # get a start and end point for the scramble
    positions = get_random_positions_based_on_cluster_size(individual, length)

    # get the subset of the original individual that corresponds to the points
    subset = individual[positions[0]:positions[1]]

    # shuffle the points
    random.shuffle(subset)

    # return the mutant
    return individual[:positions[0]] + subset + individual[positions[1]:]


MUTATION_FUNCTIONS = {
    "scramble": scramble,
    "inversion": inversion_swap,
    "insertion": insertion_mutation,
    "permutation_swap": permutation_swap,
    "two_opt": two_opt_swap,
    "cyclic": cyclic,
}
