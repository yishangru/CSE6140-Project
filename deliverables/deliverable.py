"""
algorithm result analysis and graph generation
"""
import os, shutil
import math
import time
import numpy
import pandas
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
palette = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628", "#f781bf", "#999999"]  # palette = plt.get_cmap('Set1')


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
                 label=str(round(quality * 100, 1)) + "%")
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
def sqd(graph_instance, alg, trace):
    timestamp_list = parameter_dict["sqd"]["time"][graph_instance][alg]

    # calculate quality data
    optimal = optimalVC[graph_instance]
    time_result_list = dict()
    for i, timestamp in enumerate(timestamp_list):
        reach = list()
        for seed in trace.keys():
            # binary search for reached size given timestamp
            result = trace[seed]
            start, end = 0, len(result) - 1
            if result[end][0] <= timestamp:
                reach.append(result[end][1])
                continue
            if result[start][0] > timestamp:
                print("Initial Sol takes longer than " + str(timestamp) + " , seed:" + str(seed))
                continue
            while start < end - 1:
                mid = (start + end) // 2
                if result[mid][0] < timestamp:
                    start = mid
                elif result[mid][0] > timestamp:
                    end = mid
                else:
                    start = mid
                    break
            reach.append(result[start][1])
        reach.sort()
        time_result_list[i] = reach

    print(time_result_list)

    max_cover_error = round(100 * (max([max(time_result_list[i]) for i in time_result_list.keys()]) - optimal)/optimal, 2)
    min_cover_error = round(100 * (min([min(time_result_list[i]) for i in time_result_list.keys()]) - optimal)/optimal, 2)

    print(max_cover_error)
    print(min_cover_error)

    # plot srd
    for i, timestamp in enumerate(timestamp_list):
        qualityX = [0] + [round(100 * (vc - optimal) / optimal, 2) for vc in time_result_list[i]] + \
                   [max_cover_error]
        probY = [0] + [round((j + 1) / len(trace), 4) for j in range(len(time_result_list[i]))] + [1]
        plt.plot(qualityX, probY,
                 color=palette[i],
                 linestyle='-',
                 linewidth=4,
                 label=str(timestamp))
        # marker=markers[i], markersize=3, markerfacecolor='None', markeredgewidth=2

    # set xlim and ylim
    min_padding, max_padding = parameter_dict["sqd"]["padding"][graph_instance]
    plt.xlim([min_cover_error - min_padding, max_cover_error + max_padding])
    plt.ylim([0, 1.01])

    ax = plt.gca()
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(size=5, width=2)
        axis.set_major_formatter(ScalarFormatter())
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.grid(color="black", linestyle="--", linewidth=1.8, alpha=0.9)

    plt.title("SQDs (" + alg + ") - " + graph_instance, loc='center', fontdict=title_font, pad=10)
    plt.xlabel("Relative Error (%)", fontdict=label_font)
    plt.ylabel("P (solve)", fontdict=label_font)
    plt.legend(loc=4, ncol=1, prop={'size': 14}, frameon=False)
    plt.tight_layout()
    plt.savefig('SQD-' + graph_instance + "-" + alg + '.png', dpi=600)
    plt.show()


# plot boxplot for runtime
def boxplot_runtime(graph_instance, alg, trace):
    quality_list = parameter_dict["boxtime"]["quality"][graph_instance][alg]

    optimal = optimalVC[graph_instance]
    quality_result_list = list()
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
                mid = (start + end) // 2
                if result[mid][1] < cutoff:
                    end = mid
                elif result[mid][1] > cutoff:
                    start = mid
                else:
                    end = mid
                    break
            reach.append(result[end][0])
        reach.sort()
        quality_result_list.append(reach)

    # Create an axes instance
    ax = plt.gca()

    labels = [str(round(100 * quality, 1)) for quality in quality_list]

    # add patch_artist=True option to ax.boxplot()
    bp = ax.boxplot(quality_result_list, patch_artist=True)

    # change outline color, fill color and linewidth of the boxes
    for i, box in enumerate(bp['boxes']):
        # change outline color
        box.set(color=palette[i], linewidth=2)
        # change fill color
        box.set(facecolor=palette[i])

    # change color and linewidth of the whiskers
    for i, whisker in enumerate(bp['whiskers']):
        whisker.set(color='black', linewidth=4)

    # change color and linewidth of the caps
    for i, cap in enumerate(bp['caps']):
        cap.set(color=palette[i//2], linewidth=4)

    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)

    # change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', markersize=5, markerfacecolor='None', markeredgewidth=3)

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(size=5, width=2)
        axis.set_major_formatter(ScalarFormatter())
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.grid(color="black", linestyle="--", linewidth=1.8, alpha=0.9)
    ax.set_xticklabels(labels)

    plt.title("Run Time Box Plots (" + alg + ") - " + graph_instance, loc='center', fontdict=title_font, pad=10)
    plt.xlabel("Relative Error (%)", fontdict=label_font)
    plt.ylabel("Run Time (CPU sec)", fontdict=label_font)
    plt.tight_layout()

    instance = 'box-runtime-' + graph_instance + "-" + alg
    plt.savefig(instance + '.png', dpi=600)
    plt.show()

    def get_box_plot_data(labels, bp):
        rows_list = []

        for i in range(len(labels)):
            dict1 = {}
            dict1['label'] = labels[i]
            dict1['lower_whisker'] = bp['whiskers'][i * 2].get_ydata()[1]
            dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
            dict1['median'] = bp['medians'][i].get_ydata()[1]
            dict1['upper_quartile'] = bp['boxes'][i].get_ydata().max()
            dict1['upper_whisker'] = bp['whiskers'][(i * 2) + 1].get_ydata()[1]
            rows_list.append(dict1)

        return pandas.DataFrame(rows_list)

    bp_meta = ax.boxplot(quality_result_list)
    print("Box Plot Run Time Meta:")
    meta_info = str(get_box_plot_data(labels, bp_meta))
    print(meta_info)
    with open(instance + ".meta", mode="w", encoding="utf-8") as meta:
        meta.write(meta_info + "\n")


# plot boxplot for sol size
def boxplot_solution(graph_instance, alg_list):
    result = list()
    for alg in alg_list:
        alg_result = list()
        trace = readTrace(graph_instance, alg)
        for seed in trace.keys():
            alg_result.append(trace[seed][-1][1])
        result.append(alg_result)

    print(result)

    # Create an axes instance
    ax = plt.gca()

    # add patch_artist=True option to ax.boxplot()
    bp = ax.boxplot(result, widths=0.8)

    # change outline color, fill color and linewidth of the boxes
    for i, box in enumerate(bp['boxes']):
        # change outline color
        box.set(color=palette[i], linewidth=2)

    # change color and linewidth of the whiskers
    for i, whisker in enumerate(bp['whiskers']):
        whisker.set(color='black', linewidth=4)

    # change color and linewidth of the caps
    for i, cap in enumerate(bp['caps']):
        cap.set(color=palette[i // 2], linewidth=4)

    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)

    # change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', markersize=5, markerfacecolor='None', markeredgewidth=3)

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(size=5, width=2)
        axis.set_major_formatter(ScalarFormatter())
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.grid(color="black", linestyle="--", linewidth=1.8, alpha=0.9)
    ax.set_xticklabels(alg_list)

    plt.title("VC Box Plots (cutoff=600s) - " + graph_instance, loc='center', fontdict=title_font, pad=10)
    plt.ylabel("Vertex Cover", fontdict=label_font)
    plt.tight_layout()

    instance = 'box-result-' + graph_instance
    plt.savefig(instance + '.png', dpi=600)
    plt.show()

    def get_box_plot_data(labels, bp):
        rows_list = []

        for i in range(len(labels)):
            dict1 = {}
            dict1['label'] = labels[i]
            dict1['lower_whisker'] = bp['whiskers'][i * 2].get_ydata()[1]
            dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
            dict1['median'] = bp['medians'][i].get_ydata()[1]
            dict1['upper_quartile'] = bp['boxes'][i].get_ydata().max()
            dict1['upper_whisker'] = bp['whiskers'][(i * 2) + 1].get_ydata()[1]
            rows_list.append(dict1)

        return pandas.DataFrame(rows_list)

    print("Box Plot Run Time Meta:")
    meta_info = str(get_box_plot_data(alg_list, bp))
    print(meta_info)
    with open(instance + ".meta", mode="w", encoding="utf-8") as meta:
        meta.write(meta_info + "\n")


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
            min_error = (min([trace_result[seed][-1][1] for seed in trace_result.keys()]) -
                         optimalVC[plot_graph]) / optimalVC[plot_graph]
            max_error = (max([trace_result[seed][-1][1] for seed in trace_result.keys()]) -
                         optimalVC[plot_graph]) / optimalVC[plot_graph]
            print("Graph:\n" + "Min Error: " + str(min_error) + "\n" + "Max Error: " + str(max_error))
            qrtd(plot_graph, plot_alg, trace_result)

            # plot sqd
            min_time = min([trace_result[seed][-1][0] for seed in trace_result.keys()])
            max_time = max([trace_result[seed][-1][0] for seed in trace_result.keys()])
            print("Graph:\n" + "Max Time: " + str(max_time) + "\n" + "Min Time: " + str(min_time))
            sqd(plot_graph, plot_alg, trace_result)

            # plot box for result
            boxplot_runtime(plot_graph, plot_alg, trace_result)

    # plot box for run time
    for graph in graph_list:
        boxplot_solution(graph, alg_list)


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
            "star2": (0.98, 1.52)
        }
    },
    "sqd": {
        "time": {
            "power": {
                "LS1": [6, 8, 10, 16, 24, 40, 60],
                "LS2": [40, 50, 60, 70, 80, 90, 100]
            },
            "star2": {
                "LS1": [30, 40, 50, 100, 150, 200, 300],
                "LS2": [80, 100, 125, 150, 175, 200, 225]
            }
        },
        "padding": {
            "power": (0.02, 0.1),
            "star2": (0.05, 0.05)
        }
    },
    "boxtime": {
        "quality": {
            "power": {
                "LS1": [0, 0.0005, 0.001, 0.002, 0.004],
                "LS2": [0.005, 0.01, 0.016, 0.023, 0.03]
            },
            "star2": {
                "LS1": [0, 0.0005, 0.001, 0.002, 0.004, 0.008],
                "LS2": [0.015, 0.018, 0.022, 0.026, 0.03]
            }
        }
    }
}


if __name__ == '__main__':
    main()
