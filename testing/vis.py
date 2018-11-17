import statistics

import matplotlib.pyplot as plt
import numpy as np

dataset = {0: (20833.3333, 17100.0), 1: (20900.0, 17066.6667), 2: (21300.0, 13016.6667), 3: (21600.0, 14150.0),
           4: (21600.0, 14966.6667), 5: (21600.0, 16500.0), 6: (22183.3333, 13133.3333), 7: (22583.3333, 14300.0),
           8: (22683.3333, 12716.6667), 9: (23616.6667, 15866.6667), 10: (23700.0, 15933.3333),
           11: (23883.3333, 14533.3333)}

distance_matrix = [
    [0.0, 74.53561415712697, 4109.913459889123, 3047.9957068357057, 2266.911731360042, 973.5388173508504,
     4190.100799370928, 3301.893396219811, 4757.742197606854, 3044.3481805543315, 3094.978054490498,
     3986.2611491081325],
    [74.53561415712697, 0.0, 4069.7051490249282, 2999.4907299221477, 2213.594362117867, 900.617093380362,
     4137.397248808054, 3238.5267681119735, 4701.359128899738, 2969.8952774279605, 3020.6695608019695,
     3913.8287768430096],
    [4109.913459889123, 4069.7051490249282, 0.0, 1172.3669941144244, 1972.9419656948858, 3496.2280930867328,
     891.0043851993363, 1814.907357905019, 1415.4896745963517, 3672.797925136761, 3777.1608458676424,
     2995.6449246271563],
    [3047.9957068357057, 2999.4907299221477, 1172.3669941144244, 0.0, 816.6666999999998, 2350.0, 1172.1300771577264,
     994.7081878062967, 1796.6789885168073, 2648.3748106674375, 2755.0458542261854, 2315.2873207828384],
    [2266.911731360042, 2213.594362117867, 1972.9419656948858, 816.6666999999998, 0.0, 1533.3333000000002,
     1923.8994501907957, 1188.0188835947754, 2497.2206628347617, 2208.380533080496, 2311.8054233770545,
     2324.088809500283],
    [973.5388173508504, 900.617093380362, 3496.2280930867328, 2350.0, 1533.3333000000002, 0.0, 3416.829291576882,
     2409.7602326557067, 3935.38078180216, 2113.777577650446, 2175.1117554941607, 3013.5342818321765],
    [4190.100799370928, 4137.397248808054, 891.0043851993363, 1172.1300771577264, 1923.8994501907957,
     3416.829291576882, 0.0, 1233.3333648648647, 650.8540969799302, 3086.3499657542284, 3184.380297465881,
     2202.271554554524],
    [3301.893396219811, 3238.5267681119735, 1814.907357905019, 994.7081878062967, 1188.0188835947754,
     2409.7602326557067, 1233.3333648648647, 0.0, 1586.4880519212525, 1876.7584992333072, 1978.5656895280945,
     1320.7741778551283],
    [4757.742197606854, 4701.359128899738, 1415.4896745963517, 1796.6789885168073, 2497.2206628347617,
     3935.38078180216, 650.8540969799302, 1586.4880519212525, 0.0, 3285.3631816825923, 3373.5078470998783,
     2177.21784292605],
    [3044.3481805543315, 2969.8952774279605, 3672.797925136761, 2648.3748106674375, 2208.380533080496,
     2113.777577650446, 3086.3499657542284, 1876.7584992333072, 3285.3631816825923, 0.0, 106.7186696152543,
     1359.7385892557131],
    [3094.978054490498, 3020.6695608019695, 3777.1608458676424, 2755.0458542261854, 2311.8054233770545,
     2175.1117554941607, 3184.380297465881, 1978.5656895280945, 3373.5078470998783, 106.7186696152543, 0.0,
     1411.95293791574],
    [3986.2611491081325, 3913.8287768430096, 2995.6449246271563, 2315.2873207828384, 2324.088809500283,
     3013.5342818321765, 2202.271554554524, 1320.7741778551283, 2177.21784292605, 1359.7385892557131,
     1411.95293791574, 0.0]]
pop_size = 20
generation = 20


def main():
    # generate an array of individuals and their fitnesses
    population = gen_population()
    fitness = eval_population(population)

    # plot the path
    # figure out a way to make this look nicer
    # ideas: change the color of the line progressively, etc
    fig, ax = plt.subplots()
    x = []
    y = []
    # add each city to the plot in order
    for i in range(len(population[0])):
        x.append(dataset[population[0][i]][0])
        y.append(dataset[population[0][i]][1])
    # add the first city to connect to the last
    x.append(dataset[population[0][0]][0])
    y.append(dataset[population[0][0]][1])
    plt.plot(x, y, '-o')
    plt.show()
    update(generation, fitness)

    # also, maybe some graphs that will show the max, average, and std deviation of the fitnesses over time
    # might want to generate a new population for each point to put on the graph

    return


def gen_population():
    population = []
    chromosome_length = len(dataset)
    chromosome_range = range(chromosome_length)

    for i in range(0, pop_size):
        population.append(np.random.permutation(chromosome_range))

    return population


def eval_population(population):
    fitness = []
    for individual_idx in range(len(population)):
        individual_sum = 0
        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]
        fitness.append(-individual_sum)
    return fitness


def absFit(fitness):
    absFitness = []
    for i in range(len(fitness)):
        absFitness.append(abs(fitness[i]))
    return absFitness


def maxFitness(fitness):
    absFitness = []
    for i in range(len(fitness)):
        absFitness.append(abs(fitness[i]))
    return max(absFitness)


def AvgFitness(fitness):
    absFitness = []
    for i in range(len(fitness)):
        absFitness.append(abs(fitness[i]))
    return np.mean(absFitness)


def stdDevFitness(fitness):
    absFitness = []
    for i in range(len(fitness)):
        absFitness.append(abs(fitness[i]))

    return ((statistics.stdev(absFitness)))


def update(generation, fitness):
    z = []
    meanfit = []
    stdDev = []
    maxFit = []

    for i in range(1, generation):
        z.append(i)

        meanfit.append(AvgFitness(fitness))

        stdDev.append(stdDevFitness(fitness))

        maxFit.append(maxFitness(fitness))
        i = i + 1
    plt.plot(z, meanfit, 'g^')
    plt.plot(z, stdDev, 'r+')
    plt.plot(z, maxFit, 'go--')
    plt.xlabel('Number of Generations')
    plt.ylabel('Standard Deviation, Mean and Maximum Fitness')
    plt.title('Fitness Comparisons Over Generations')
    plt.show()

    return


# run main
if __name__ == "__main__":
    main()
