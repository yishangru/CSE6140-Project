"""
algorithm result analysis and graph generation
"""
import os, shutil
import math
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

target_result_directory = "result"
original_result_directory = "../result/1"

# extract result file from original dir, e.g - extractResult("power", "LS1")
def extractResult(graph_instance, alg):
    if not (os.path.exists(target_result_directory) and os.path.isdir(target_result_directory)):
        os.mkdir(target_result_directory)
    if not (os.path.exists(original_result_directory) and os.path.isdir(original_result_directory)):
        print("Original Result Directory Not Exist! Dir: " + original_result_directory)
        return

    # extract result trace and sol
    file_list = os.listdir(original_result_directory)
    for result in file_list:
        file_info = result.split("_")
        file_algorithm = file_info[len(file_info) - 3]
        file_graph_instance = "_".join(file_info[:len(file_info) - 3])
        if not (file_algorithm == alg and file_graph_instance == graph_instance):
            continue
        shutil.copyfile(os.path.join(original_result_directory, result), os.path.join(target_result_directory, result))


optimalVC = {
    "jazz": 158,
    "karate": 14,
    "football": 94,
    "as-22july06": 3303,
    "hep-th": 3926,
    "star": 6902,
    "star2": 4542,
    "netscience": 899,
    "email": 594,
    "delaunay_n10": 703,
    "power": 2203,
    "dummy1": 2,
    "dummy2": 3
}

title_font = {
    'family': 'Comic Sans MS',
    'weight': 'bold',
    'size': 20,
}

label_font = {
    'family': 'Comic Sans MS',
    'weight': 'bold',
    'size': 15,
}

plot_font = {
    'family': 'Comic Sans MS',
    'weight': 'heavy',
    'size': 12,
}

markers = ["o", "v", "s", "p", "X", "*", "P", "H", "d"]
matplotlib.rc('font', **plot_font)
plt.style.use('seaborn-bright')
palette = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628"]  # palette = plt.get_cmap('Set1')


def readTrace(graph_instance, alg):
    graph_result_list = list()

    # extract result trace name
    result_file_list = os.listdir(target_result_directory)
    for result_file in result_file_list:
        file_info = result_file.split("_")
        file_type = result_file.split(".")[-1]
        file_algorithm = file_info[len(file_info) - 3]
        file_graph_instance = "_".join(file_info[:len(file_info) - 3])
        if not (file_algorithm == alg and file_graph_instance == graph_instance and file_type == "trace"):
            continue
        graph_result_list.append(result_file)

    # read trace result
    trace_result = dict()
    for graph_result in graph_result_list:
        file_info = graph_result.split("_")
        random_seed = int(graph_result.split("_")[len(file_info) - 1].split(".")[0])
        with open(os.path.join(target_result_directory, graph_result), mode="r", encoding="utf-8") as result:
            trace = result.readlines()
            trace_result[random_seed] = list()
            for i, line in enumerate(trace):
                content = line.split(",")
                trace_result[random_seed].append((float(content[0]), int(content[1])))

    return trace_result


# plot QRTD
def qrtd(graph_instance, alg, trace):
    quality_list = parameter_dict["qrtd"]["quality"][graph_instance][alg]

    # calculate quality data
    optimal = optimalVC[graph_instance]
    quality_result_list = dict()
    for i, quality in enumerate(quality_list):
        cutoff = math.floor(quality * optimal + optimal)
        reach = list()
        for seed in trace.keys():
            # binary search for expected timestamp
            result = trace[seed]
            start, end = 0, len(result) - 1
            if result[start][1] <= cutoff:
                reach.append(result[start][0])
                continue
            if result[end][1] > cutoff:
                continue
            while start < end - 1:
                mid = (start + end)//2
                if result[mid][1] < cutoff:
                    end = mid
                elif result[mid][1] > cutoff:
                    start = mid
                else:
                    end = mid
                    break
            reach.append(result[end][0])
        reach.sort()
        quality_result_list[i] = reach

    print(quality_result_list)

    max_time = max([max(quality_result_list[i]) for i in quality_result_list.keys()])
    min_time = min([min(quality_result_list[i]) for i in quality_result_list.keys()])

    # plot qrtd
    for i, quality in enumerate(quality_list):
        timeX = [min_time] + quality_result_list[i] + [max_time]
        probY = [0] + [round((j + 1)/len(trace), 4) for j in range(len(quality_result_list[i]))] + [1]
        plt.plot(timeX, probY,
                 color=palette[i],
                 linestyle='-.',
                 linewidth=4,
                 label=str(quality) + "%")
        # marker=markers[i], markersize=3, markerfacecolor='None', markeredgewidth=2

    # set xlim and ylim
    min_padding, max_padding = parameter_dict["qrtd"]["padding"][graph_instance]
    plt.xlim([round(min_time * min_padding), round(max_time * max_padding)])
    plt.ylim([0, 1.01])

    ax = plt.gca()
    plt.xscale("log")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(size=5, width=2)
        axis.set_major_formatter(ScalarFormatter())
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.grid(color="black", linestyle="--", linewidth=1.8, alpha=0.9)

    plt.title("Qualified RTDs (" + alg + ") - " + graph_instance, loc='center', fontdict=title_font, pad=10)
    plt.xlabel("Run Time (CPU sec)", fontdict=label_font)
    plt.ylabel("P (solve)", fontdict=label_font)
    plt.legend(loc=4, ncol=1, prop={'size': 14}, frameon=False)
    plt.tight_layout()
    plt.savefig('QRTD-' + graph_instance + "-" + alg + '.png', dpi=600)
    plt.show()


# plot SQD
def sqd(graph_instance, alg, timestamp_list):
    pass


# plot boxplot for runtime
def boxplot_runtime(graph_instance, alg):
    pass


# plot boxplot for sol size
def boxplot_solution(graph_instance, alg):
    pass


def main():
    # extract result from original directory
    graph_list = ["power", "star2"]
    alg_list = ["LS1", "LS2"]

    for plot_graph in graph_list:
        for plot_alg in alg_list:
            extractResult(plot_graph, plot_alg)
            time.sleep(1)

            trace_result = readTrace(plot_graph, plot_alg)

            # plot qrtd
            min_error = (min([min(trace_result[seed], key=lambda x: x[1])[1] for seed in trace_result.keys()]) -
                         optimalVC[plot_graph]) / optimalVC[plot_graph]
            max_error = (max([max(trace_result[seed], key=lambda x: x[1])[1] for seed in trace_result.keys()]) -
                         optimalVC[plot_graph]) / optimalVC[plot_graph]
            print("Graph:\n" + "Min: " + str(min_error) + "\n" + "Max: " + str(max_error))
            qrtd(plot_graph, plot_alg, trace_result)


parameter_dict = {
    "qrtd": {
        "quality": {
            "power": {
                "LS1": [0, 0.001, 0.003, 0.006, 0.01],
                "LS2": [0.01, 0.015, 0.02, 0.025, 0.03]
            },
            "star2": {
                "LS1": [0, 0.001, 0.003, 0.005, 0.008, 0.01],
                "LS2": [0.015, 0.018, 0.022, 0.026, 0.03]
            }
        },
        "padding": {
            "power": (0.98, 1.3),
            "star2": (0.98, 1.5)
        }
    }
}

# read data random seed: trace list
"""
plot_graph, plot_alg = "star2", "LS2"
time.sleep(1)  # sleep one second
trace_result_1 = readTrace(plot_graph, plot_alg)

# plot qrtd
min_error = (min([min(trace_result_1[seed], key=lambda x: x[1])[1] for seed in trace_result_1.keys()]) - optimalVC[plot_graph]) / optimalVC[plot_graph]
max_error = (max([max(trace_result_1[seed], key=lambda x: x[1])[1] for seed in trace_result_1.keys()]) - optimalVC[plot_graph]) / optimalVC[plot_graph]
print("Graph:\n" + "Min: " + str(min_error) + "\n" + "Max: " + str(max_error))
qrtd(plot_graph, plot_alg, trace_result_1)""
"""

if __name__ == '__main__':
    main()
