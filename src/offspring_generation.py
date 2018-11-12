import random


def recombination(args):
    population = args['population']
    parents = args['mating_pool']
    mp_size = args['mp_size']
    crossover_rate = args['crossover_rate']

    if args['recombination'] == 'cut_crossfill':
        offspring = []
        i = 0

        while len(offspring) < mp_size:
            parent1 = population[parents[i]]
            parent2 = population[parents[i + 1]]

            if random.random() < crossover_rate:
                offspring1, offspring2 = cut_crossfill(args, list(parent1), list(parent2))
            else:
                offspring1 = list(population[parents[i]].copy())
                offspring2 = list(population[parents[i + 1]].copy())
            offspring.append(offspring1)
            offspring.append(offspring2)

        args['offspring'] = offspring
        return


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
            offspring[i] = permutation_swap(offspring[i])


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

    pass
