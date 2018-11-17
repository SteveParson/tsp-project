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
        for i in range(pop_size):

            knn_cluster_centers = np.random.choice(range(chromosome_length), args['knn_k'])
            knn_cluster_cities = [[] for x in range(args['knn_k'])]

            for city in range(chromosome_length):
                distances = [distance_matrix[x][city] for x in knn_cluster_centers]
                min_d = np.argmin(distances)
                knn_cluster_cities[min_d].append(city)

            # print("KNN Cluster Centers: ", knn_cluster_centers)
            # print("KNN Cluster Cities: ", knn_cluster_cities)
            ind = [knn_cluster_cities[x][y] for x in range(len(knn_cluster_cities)) for y in
                   range(len(knn_cluster_cities[x]))]

            # print("Individual: ", ind)
            pop.append(ind)

    args['population'] = pop
