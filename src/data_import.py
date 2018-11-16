import math


def parse_datafile(args):
    """ Parse the TSP data file

    :param args: The global parameter dictionary
    :return: Adds the 'dataset' to the dictionary
    """

    datafile = args['datafile']
    dataset = {}
    with open(datafile, 'r') as inputfile:
        for line in inputfile:
            elements = line.split()
            dataset[int(elements[0]) - 1] = (float(elements[1]), float(elements[2]))
    args['dataset'] = dataset
    print(args['dataset'])

def calc_distance_matrix(args):
    """ Calculate the distance matrix

    :param args: The global parameter dictionary
    :return: Adds the 'distance_matrix' to the dictionary
    """

    # TODO: This function is pretty expensive.

    dataset = args['dataset']
    all_cities = range(len(dataset))
    distance_matrix = [[0 for city1 in all_cities] for city2 in all_cities]

    for city1 in all_cities:
        for city2 in all_cities:
            distance_matrix[city1][city2] = math.sqrt((dataset[city1][0] - dataset[city2][0]) ** 2 + (
                    dataset[city1][1] - dataset[city2][1]) ** 2)

    args['distance_matrix'] = distance_matrix
