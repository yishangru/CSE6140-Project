"""
algorithm result analysis and graph generation
"""
import os, shutil

target_result_directory = "result"
original_result_directory = "../result/1"

# extract result file from original dir
def extractResult(graph_name, alg):
    if not (os.path.exists(target_result_directory) and os.path.isdir(target_result_directory)):
        os.mkdir(target_result_directory)
    if not (os.path.exists(original_result_directory) and os.path.isdir(original_result_directory)):
        print("Original Result Directory Not Exist! Dir: " + original_result_directory)
        return
    # extract result trace and sol
    file_list = os.listdir(original_result_directory)
    for result in file_list:
        file_info = result.split("_")
        if file_info[len(file_info) - 3] == alg:


# plot QRTD
def qrtd(graph_name, alg, quality_list):
    pass


# plot SQD
def sqd(graph_name, alg, timestamp_list):
    pass


# plot boxplot for runtime
def boxplot_runtime(graph_name, alg):
    pass


# plot boxplot for sol size
def boxplot_solution(graph_name, alg):
    pass

