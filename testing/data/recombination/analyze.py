from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def load_data_from_file(filename):
    fitnesses = []
    with open(filename) as fp:
        lines = fp.readlines()[1:]
        for line in lines:
            run_num, fitness = line.split(',')
            fitness = fitness.strip()
            fitnesses.append(float(fitness))

    return fitnesses

def compute_mann_whitney_u(datafile1, datafile2):
    data1 = load_data_from_file(datafile1)
    data2 = load_data_from_file(datafile2)
    stat, p = mannwhitneyu(data1, data2, alternative='two-sided')
    print('Statistics={:.3f}, p={:.4f}'.format(stat, p))

def visualize():
    data1 = load_data_from_file("best_order.json.csv")
    data2 = load_data_from_file("cut_crossfill.json.csv")
    indices = list(range(1, 31))

    plt.figure(1, figsize=(10.0,6.0), dpi=300)
    plt.xlabel("Runs (n=30)")
    plt.ylabel("Fitness (Euclidean distance)")
    plt.title("Best order vs. cut and crossfill")

    plt.plot(indices, data1, c='tab:orange',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data2, c='tab:green',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)

    orange_patch = mpatches.Patch(color='tab:orange', label='Best Order')
    green_patch = mpatches.Patch(color='tab:green', label='Cut And Crossfill')
    plt.legend(handles=[orange_patch, green_patch])
    plt.savefig("best_order_vs_cut_crossfill.png", dpi=300)

if __name__ == '__main__':
    compute_mann_whitney_u("best_order.json.csv",
                           "cut_crossfill.json.csv")
    visualize()
