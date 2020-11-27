#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import time
import argparse
import multiprocessing
from solution.solution import solutionExecutor
from utils.data import checkData, readData, checkSol, writeSol, writeTrace

DEBUG = True
defaultProcessNum = 1
graphDataDirectory = "./data/Data"
debugResultDirectory = "./result"  # writing directory when DEBUG

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', type=str, required=True,
                        help="graph data path")
    parser.add_argument('-alg', type=str, required=True,
                        help="algorithm [BnB|Approx|ApproxUpdate|LS1|LS2|NetworkX]")
    parser.add_argument('-time', type=int, default=600,
                        help="time limit for algorithm run, default 600")
    parser.add_argument('-seed', type=int, default=123,
                        help="random seed, default 123")
    parser.add_argument('-rc', type=int, default=1,
                        help="algorithm running repeat count")
    parser.add_argument('-cd', '--checkData', action="store_true", default=False,
                        help="check graph data validity")
    parser.add_argument('-cs', '--checkSol', action="store_true", default=False,
                        help="check solution completeness")
    parser.add_argument('-ba', '--batchRun', action="store_true", default=False,
                        help="run same setting for each data graph")
    parser.add_argument('-params', type=str, default="{}",
                        help="parameter string for algorithm parameter setting in JSON, "
                             "e.g. '{\"para1\": 3, \"para2\": [\"str\", 1, 3.5]}'")

    args = parser.parse_args()

    if not (os.path.exists(args.inst) and os.path.isfile(args.inst)):
        print("File Path Invalid - " + args.inst)
        return

    target_graph_list = list()

    if args.batchRun:
        graph_file_list = os.listdir(graphDataDirectory)
        for graph in graph_file_list:
            split_name = graph.split(".")
            if len(split_name) == 2 and split_name[1] == "graph":
                target_graph_list.append(graphDataDirectory + "/" + graph)
    else:
        target_graph_list.append(args.inst)

    # make directory for debug running results
    if DEBUG:
        if not (os.path.exists(debugResultDirectory) and os.path.isdir(debugResultDirectory)):
            os.mkdir(debugResultDirectory)

    for i in range(len(target_graph_list)):
        graph_path = target_graph_list[i]

        print("Current Running [ " + graph_path + " ]")

        # check graph valid
        if args.checkData:
            print("Checking graph valid ...")
            print("Graph Data [ " + graph_path + " ] " + ("Valid" if checkData(graph_path) else "Invalid"))
            print()
            continue

        # add graph name, and optimal for cutoff
        graph_instance = graph_path.split("/")[-1].split(".")[0]
        # print(args.params[1:-1] == '{"T":0.9,"steps":10000,"alpha":0.999}')
        param_json = json.loads(args.params[1:-1])
        param_json["graph_name"] = graph_instance
        param_json["opt"] = optimalVC[graph_instance] if graph_instance in optimalVC.keys() else 0

        # ./result/ if DEBUG else .
        for run_count in range(1, args.rc + 1):
            write_dir = "."
            if DEBUG:
                write_dir = os.path.join(debugResultDirectory, str(run_count))
                if not (os.path.exists(write_dir) and os.path.isdir(write_dir)):
                    os.mkdir(write_dir)
            # running algorithm
            print("Start running [" + str(run_count) + "] ...")
            run(args, param_json, graph_path, write_dir)

        print("Finish running [ " + graph_path + " ] ...\n")


def run(args, params, graph_path, write_dir):

    # start running
    start_time = time.time()

    # read data
    graph = readData(graph_path)

    """
        Using multiprocessing for possible multiple process concurrent running.
        Multiprocessing will serialize and deserialize the argument (deep copy). 
        Thus, each process will have it independent memory space (not affect other).
        Set time limit as args.time - 2, allowing solution select and output tasks. 
    """
    params_tuple = (graph, args.alg, args.time - 2, args.seed, params, start_time)
    process_pool = multiprocessing.Pool(processes=defaultProcessNum)
    # shallow copy for parameter passing
    retrieved_sols = process_pool.starmap(solutionExecutor, [params_tuple for i in range(defaultProcessNum)])
    # not join to allow termination, main thread keep going once having return value
    # process_pool.join()
    process_pool.close()

    # check solution validity
    if args.checkSol:
        print("Checking solution validity ...")
        for solution in range(len(retrieved_sols)):
            if checkSol(graph_path, retrieved_sols[solution][0]):
                print("Solution " + str(solution) + " check: valid")
                continue
            print("Solution " + str(solution) + " check: fail")

    # select best
    current_best = retrieved_sols[0]
    for solution in range(1, len(retrieved_sols)):
        if len(retrieved_sols[solution][0]) < len(current_best[0]):
            current_best = retrieved_sols[solution]
    # TODO: Change file name for BnB
    write_result_path = os.path.join(write_dir, params["graph_name"] + "_" + args.alg + "_"
                                     + str(args.time) + (("_" + str(args.seed)) if not (args.seed == -1) else ""))
    # write vertex set
    writeSol(writePath=write_result_path + ".sol", vertexSet=current_best[0])
    # write trace
    writeTrace(writePath=write_result_path + ".trace", traceList=current_best[1])


if __name__ == "__main__":
    main()
