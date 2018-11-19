import math
import os.path
import pickle
import sys


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

def calc_distance_matrix(args):
    """ Calculate the distance matrix

    :param args: The global parameter dictionary
    :return: Adds the 'distance_matrix' to the dictionary
    """

    # TODO: This function is pretty expensive.

    dataset = args['dataset']

    # load the distance matrix from a file if it exists
    if os.path.isfile(sys.argv[1] + ".distance"):
        with open(sys.argv[1] + ".distance", "rb") as myfile:
            distance_matrix = pickle.load(myfile)

    else:
        all_cities = range(len(dataset))
        distance_matrix = [[0 for city1 in all_cities] for city2 in all_cities]

        for city1 in all_cities:
            for city2 in all_cities:
                distance_matrix[city1][city2] = math.sqrt((dataset[city1][0] - dataset[city2][0]) ** 2 + (
                        dataset[city1][1] - dataset[city2][1]) ** 2)

        # write the distance matrix to a file
        f = open(sys.argv[1] + ".distance", "wb")
        pickle.dump(distance_matrix, f)
        f.close()

    args['distance_matrix'] = distance_matrix
