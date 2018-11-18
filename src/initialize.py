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
        for i in range(pop_size):
            pop.append(kmeans(args))

        # multi process
        # pool = mp.Pool(processes=6)
        # results = [pool.apply_async(kmeans, args=(args,)) for x in range(pop_size)]
        # pop = [p.get() for p in results]
        # for p in pop:
        #     print(p)



    args['population'] = pop


def kmeans(args):
    np.random.seed()
    chromosome_length = len(args['dataset'])
    distance_matrix = args['distance_matrix']
    knn_cluster_centers = np.random.choice(range(chromosome_length), args['knn_k'], replace=False)
    knn_cluster_cities = [[] for x in range(args['knn_k'])]

    for city in range(chromosome_length):
        distances = [distance_matrix[x][city] for x in knn_cluster_centers]
        min_d = np.argmin(distances)
        knn_cluster_cities[min_d].append(city)

    print("KNN Cluster Centers: ", knn_cluster_centers)
    print("KNN Cluster Cities: ", knn_cluster_cities)

    # for each cluster, figure out which one is at the center
    convergence_value = 1000000
    last_convergence_val = 100000

    while True:
        print("Last convergence value:", (last_convergence_val - convergence_value))
        last_convergence_val = convergence_value
        convergence_value = 0

        for cluster_idx in range(len(knn_cluster_cities)):
            print("KNN Cluster Centers: ", knn_cluster_centers)
            print("KNN Cluster Cities: ", knn_cluster_cities)
            print("Considering cluster %d: %s" % (cluster_idx, knn_cluster_cities[cluster_idx]))
            if len(knn_cluster_cities[cluster_idx]) == 0:
                continue
            distances = []
            distance = 0
            for city_idx in range(len(knn_cluster_cities[cluster_idx])):
                for city_idx2 in range(len(knn_cluster_cities[cluster_idx])):
                    if city_idx == city_idx2:
                        continue
                    distance += distance_matrix[knn_cluster_cities[cluster_idx][city_idx]][
                        knn_cluster_cities[cluster_idx][city_idx2]]
                distances.append(distance)
            low_idx = np.argmin(distances)
            convergence_value += distances[low_idx]

            low_city = knn_cluster_cities[cluster_idx][low_idx]

            print("Distances: ", distances)
            print("Lowidx %d, low_city %d" % (low_idx, low_city))
            knn_cluster_centers[cluster_idx] = low_city

        for city in range(chromosome_length):
            knn_cluster_cities = [[] for x in range(args['knn_k'])]
            distances = [distance_matrix[x][city] for x in knn_cluster_centers]
            min_d = np.argmin(distances)
            knn_cluster_cities[min_d].append(city)
        print("Convergence: ", convergence_value)
        print("criteria ", (last_convergence_val - convergence_value))
        print("KNN Cluster Centers: ", knn_cluster_centers)
        print("KNN Cluster Cities: ", knn_cluster_cities)

        print()

        x = input()

    raise SystemExit

    x = [knn_cluster_cities[x][y] for x in range(len(knn_cluster_cities)) for y in
         range(len(knn_cluster_cities[x]))]

    # print(x)
    return x
