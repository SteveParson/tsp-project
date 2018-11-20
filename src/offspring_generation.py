import random

from .utility import *


def recombination(args):
    population = args['population']
    parents = args['mating_pool']
    mp_size = args['mp_size']
    crossover_rate = args['crossover_rate']
    recombination_type = args['recombination']
    fitness = args['fitness']
    popsize = args['pop_size']

    if recombination_type == 'cut_crossfill':
        offspring = []
        i = 0
        while len(offspring) < popsize:
            parent1 = population[parents[i]]
            parent2 = population[parents[i + 1]]
            if random.random() < crossover_rate:
                offspring1, offspring2 = cut_crossfill(args, list(parent1), list(parent2))
            else:
                offspring1 = list(population[parents[i]].copy())
                offspring2 = list(population[parents[i + 1]].copy())
            offspring.append(offspring1)
            offspring.append(offspring2)

    if recombination_type == 'best_order':
        best_individual = population[np.argmax(fitness)]

        n = args['box_cutting_points_n']
        J = len(population[0])

        if not (2 <= n <= J - 1):
            die("box_cutting_points_n is out of range")

        offspring = []
        i = 0

        while len(offspring) < mp_size:
            # print("Parents i ", parents[i])
            # print("Parents i ", parents[i+1])
            # print("Population  ", population[parents[i]])
            parent1 = population[parents[i]]
            parent2 = population[parents[i + 1]]
            if random.random() < crossover_rate:
                offspring1, offspring2 = best_order(args, J, n, parent1, parent2, best_individual)
            else:
                offspring1 = list(population[parents[i]].copy())
                offspring2 = list(population[parents[i + 1]].copy())

            offspring.append(offspring1)
            offspring.append(offspring2)

    args['offspring'] = offspring
    return


# TODO: Broken
def best_order(args, J, n, parent1, parent2, best_individual):
    """ Applies best-order crossover and produces two offspring
    using the order information from three parents.

    :param args: Our parameter dictionary
    :param J: The length of our chromosome
    :param n: The number of cutting points for crossover
    :param parent1: Our first parent
    :param parent2: The second parent
    :param best_individual: The best individual in our population
    :return: Two offspring
    """

    q = [0]
    for i in range(n):
        q.append(q[i] + random.randint(1, (J // 3)))
    q.append(J - 1)
    q.sort()

    bad_cutting_point_sequence = True
    while bad_cutting_point_sequence:

        q = [0]
        q.extend(sorted(random.sample(range(1, J), n - 2)))
        q.append(J)

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
    # print("q: ", q)
    # print("pc: ", parent_choices)

    offspring1 = []
    offspring2 = []

    for i in range(len(q) - 1):
        sp = q[i]
        ep = q[i + 1]

        # print("i is ", i)
        if parent_choices[i] == 1:
            alleles1 = parent1[sp:ep]
            alleles2 = parent2[sp:ep]
            # print("pc1: ", parent1[sp:ep], alleles1)

        if parent_choices[i] == 2:
            alleles1 = order_subset_from_full_set(parent1[sp:ep], parent2)
            alleles2 = order_subset_from_full_set(parent2[sp:ep], parent1)
            # print("pc2: ", parent1[sp:ep], alleles1)

        if parent_choices[i] == 3:
            alleles1 = order_subset_from_full_set(parent1[sp:ep], best_individual)
            alleles2 = order_subset_from_full_set(parent2[sp:ep], best_individual)
            # print("pc3: ", parent1[sp:ep], alleles1)

        offspring1.extend(alleles1)
        offspring2.extend(alleles2)

    # print("parents: \n\t%s\n\t%s\n\t%s" %(parent1, parent2, best_individual))
    # print("offspring: \n\t%s\n\t%s " %(offspring1, offspring2))
    return offspring1, offspring2


def cut_crossfill(args, parent1, parent2):
    offspring1 = []
    offspring2 = []

    crossover_point = random.randint(0, len(parent1) - 2)

    # Offspring 1
    allele_index = crossover_point + 1
    # Copy until the crossover point from parent1
    offspring1 = parent1[0: allele_index]

    # Fill the other half of offspring until full
    while len(offspring1) != len(parent1):
        # Grab an allele from parent2
        parent_allele = parent2[allele_index]

        # if it's not in offspring1, put it there
        if parent_allele not in offspring1:
            offspring1.append(parent_allele)

        # increment and wrap around index pointer
        allele_index = (allele_index + 1) % len(parent2)

    # as above
    allele_index = crossover_point + 1
    offspring2 = parent2[0: allele_index]
    while len(offspring2) != len(parent2):
        parent_allele = parent1[allele_index]
        if parent_allele not in offspring2:
            offspring2.append(parent_allele)
        allele_index = (allele_index + 1) % len(parent1)

    return offspring1, offspring2


def mutation(args):
    mutation_rate = args['mutation_rate']
    offspring = args['offspring']

    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = inversion_swap(offspring[i])

def permutation_swap(individual):
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

def insertion_mutation(individual):
    z = [random.randint(0, len(individual) - 1) for x in range(2)]
    z.sort()
    mutant = individual[:z[0]] + individual[z[0] + 1:z[1] + 1]
    mutant.append(individual[z[0]])
    mutant.extend(individual[z[1] + 1:])
    return mutant

def inversion_swap(individual):
    z = [random.randint(0, len(individual)-1) for x in range(2)]
    z.sort()
    seq = individual[z[0]:z[1] + 1]
    seq.reverse()
    mutant = individual[:z[0]] + seq + individual[z[1] + 1:]
    return mutant
