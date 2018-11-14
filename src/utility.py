def rankify(values):
    """ Rank an array

    :param values: An array of values
    :return: A ranking for the array of values
    """
    return list(np.argsort(np.array(values)))[::-1]
