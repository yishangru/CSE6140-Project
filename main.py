#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import time
import argparse
import multiprocessing
from solution.solution import solutionExecutor
from data import checkData, readData, checkSol, writeSol, writeTrace

defaultProcessNum = 2
graphDataDirectory = "./data/Data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cd', '--checkData', action="store_true", default=False,
                        help="check graph data validity")
    parser.add_argument('-cs', '--checkSol', action="store_true", default=False,
                        help="check solution completeness")
    parser.add_argument('-inst', type=str, required=True,
                        help="graph data path")
    parser.add_argument('-alg', type=str, required=True,
                        help="algorithm [BnB|Approx|LS1|LS2|NetworkX]")
    parser.add_argument('-time', type=int, default=-1,
                        help="Time limit for algorithm run, default no")
    parser.add_argument('-seed', type=int, default=-1,
                        help="Random seed, default -1")
    parser.add_argument('-params', type=str, default="{}",
                        help="Parameter string for algorithm parameter setting in JSON, "
                             "e.g. '{\"para1\": 3, \"para2\": [\"str\", 1, 3.5]}'")

    args = parser.parse_args()

    if not (os.path.exists(args.inst) and os.path.isfile(args.inst)):
        print("File Path Invalid - " + args.inst)
        return

    if args.checkData:
        print("Checking graph valid: " + args.inst)
        print("Graph Data " + ("Valid" if checkData(args.inst) else "Invalid"))
        return

    start_time = time.time()

    # read data
    graph = readData(args.inst)
    param_json = json.loads(args.params)

    """
        Using multiprocessing for possible multiple process concurrent running.
        Multiprocessing will serialize and deserialize the argument (deep copy). 
        Thus, each process will have it independent memory space (not affect other).
        Set time limit as args.time - 2, allowing solution select and output tasks. 
    """
    params_tuple = (graph, args.alg, args.time - 2, args.seed, param_json, start_time)
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
            if checkSol(args.inst, retrieved_sols[solution]):
                continue
            print("Solution " + str(solution) + " check: fail")

    # select best
    current_best = retrieved_sols[0]
    for solution in range(1, len(retrieved_sols)):
        if len(retrieved_sols[solution][0]) < len(current_best[0]):
            current_best = retrieved_sols[solution]

    # write vertex set
    write_path = args.inst.split("/")[-1].split(".")[0] + "_" + args.alg + "_" + str(args.time) + \
                 (("_" + str(args.seed)) if not (args.seed == -1) else "")
    writeSol(writePath=write_path + ".sol", vertexSet=current_best[0])
    writeTrace(writePath=write_path + ".trace", traceList=current_best[1])


def batchCheckData():
    graph_file_list = os.listdir(graphDataDirectory)
    print(graph_file_list)
    for graph in graph_file_list:
        split_name = graph.split(".")
        if len(split_name) == 2 and split_name[1] == "graph":
            print("Checking graph valid: " + graph)
            print("Graph Data " + ("Valid" if checkData(os.path.join(graphDataDirectory, graph)) else "Invalid"))
            print()


if __name__ == "__main__":
    main()

