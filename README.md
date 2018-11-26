# tsp-project
TSP with evolutionary algorithms

# Data Generation

Hold kmeans constant.

## Combinations

Generate 20 runs worth of data for each combination.

Holding kmeans constant, we have the following combinations:

1. K-means + best_order + cyclic mutation
2. K-means + cut_and_crossfill + cyclic mutation
3. K-means + best_order + scramble
4. K-means + best_order + inversion
5. K-means + best_order + insertion
6. K-means + best_order + permutation_swap
7. K-means + best_order + two_opt_swap
8. K-means + best_order + cyclic (with varying configurations to
   discover correlations between certain values).
