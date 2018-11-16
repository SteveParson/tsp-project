import numpy as np
import sys


def rankify(values):
    """ Rank an array

    :param values: An array of values
    :return: A ranking for the array of values
    """
    return list(np.argsort(np.array(values)))[::-1]


def order_subset_from_full_set(subset, full_set):
    """ Arranges a subset in an order defined by another set

    :param subset: A list containing the elements we wish to order
    :param full_set: A superset of subset, from which we wish to extract order information
    :return: subset, with the order from full_set
    """
    new_order = []

    for element in full_set:
        if element in subset:
            new_order.append(element)

    return new_order


def die(error):
    """ Helper function to die on error

    :param error: Error message to display to user
    :return: Kills the program
    """

    print("Error: " + error)
    print("Usage: python3.5 " + str(sys.argv[0]) +
          " datafile")
    raise SystemExit
