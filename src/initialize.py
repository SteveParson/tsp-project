import multiprocessing as mp

import numpy as np


def gen_population(args):
    chromosome_length = len(args['dataset'])
    distance_matrix = args['distance_matrix']
    pop_size = args['pop_size']
    initialize_method = args['initialize_method']
    chromosome_range = range(chromosome_length)
    pop = []

    if initialize_method == 'random':
        for i in range(pop_size):
            pop.append(np.random.permutation(chromosome_range))

    if initialize_method == 'kmeans':
        # single process
        # for i in range(pop_size):
        #    pop.append(kmeans(args))

        # multi process

        # set this too high and too much ram is used
        # https://stackoverflow.com/questions/18414020/memory-usage-keep-growing-with-pythons-multiprocessing-pool
        # problem probably not worth fixing, structural cost is high
        pool = mp.Pool(processes=3)

        results = [pool.apply_async(kmeans, args=(args,)) for x in range(pop_size)]
        pop = [p.get() for p in results]
        print(pop)
        pool.close()
        pool.join()

    args['population'] = pop


def kmeans(args):
    chromosome_length = len(args['dataset'])
    distance_matrix = args['distance_matrix']

    # because of multiprocessing, reseed
    np.random.seed()

    # get cluster centers
    knn_cluster_centers = np.random.choice(range(chromosome_length), args['knn_k'], replace=False)

    # prepare an array of cities that correspond to the centers
    knn_cluster_cities = [[] for x in range(args['knn_k'])]

    # assign every city to a particular cluster
    for city in range(chromosome_length):
        distances = [distance_matrix[x][city] for x in knn_cluster_centers]
        min_d = np.argmin(distances)
        knn_cluster_cities[min_d].append(city)

    # print("KNN Cluster Centers: ", knn_cluster_centers)
    # print("KNN Cluster Cities: ", knn_cluster_cities)

    # TODO: Need a better convergence model
    iteration = 0
    while iteration < 10:
        # print()
        # print("Iteration ", i)
        iteration += 1

        # for every cluster
        for cluster_idx in range(len(knn_cluster_cities)):
            # print("KNN Cluster Centers: ", knn_cluster_centers)
            # print("KNN Cluster Cities: ", knn_cluster_cities)
            # print("Considering cluster %d: %s" % (cluster_idx, knn_cluster_cities[cluster_idx]))

            # if this cluster is empty, skip it
            if len(knn_cluster_cities[cluster_idx]) == 0:
                continue

            distances = []
            distance = 0

            # find a new center
            for city_idx in range(len(knn_cluster_cities[cluster_idx])):
                for city_idx2 in range(len(knn_cluster_cities[cluster_idx])):
                    if city_idx == city_idx2:
                        continue
                    distance += distance_matrix[knn_cluster_cities[cluster_idx][city_idx]][
                        knn_cluster_cities[cluster_idx][city_idx2]]
                distances.append(distance)
            low_idx = np.argmin(distances)

            # convergence_value += distances[low_idx]

            # assign the new center
            low_city = knn_cluster_cities[cluster_idx][low_idx]
            knn_cluster_centers[cluster_idx] = low_city

            # print("Distances: ", distances)
            # print("Lowidx %d, low_city %d" % (low_idx, low_city))

        # remove the cluster lists
        knn_cluster_cities = [[] for x in range(args['knn_k'])]

        # reestablish the cluster lists with the new centers
        for city in range(chromosome_length):
            distances = [distance_matrix[x][city] for x in knn_cluster_centers]
            min_d = np.argmin(distances)
            knn_cluster_cities[min_d].append(city)

        # print("Convergence: ", convergence_value)
        # print("criteria ", (last_convergence_val - convergence_value))
        # print("KNN Cluster Centers: ", knn_cluster_centers)
        # print("KNN Cluster Cities: ", knn_cluster_cities)

        # print()

    flattened_array = [knn_cluster_cities[x][y] for x in range(len(knn_cluster_cities)) for y in
                       range(len(knn_cluster_cities[x]))]

    # print(x)
    return flattened_array
