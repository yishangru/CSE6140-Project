"""
Top level solution wrapper, infrastructure
"""
import time
import copy
import threading

class Solution(threading.Thread):
    def __init__(self, graph, randomSeed, startTime):
        super().__init__()
        self.graph = graph
        self.randomSeed = randomSeed
        self.lock = threading.Lock()
        # current best vertex set solution
        self.vertexSet = set()
        # record trace
        self.startTime = startTime
        self.trace = list()

    def run(self):
        raise NotImplementedError

    def updateVertexSet(self, vertexSet):
        self.lock.acquire()
        self.vertexSet = set(vertexSet)
        self.lock.release()

    def updateTrace(self, vertexSize):
        self.lock.acquire()
        self.trace.append((format(time.time() - self.startTime, '.2f'), vertexSize))
        self.lock.release()

    def getSolution(self):
        self.lock.acquire()
        vertex_sol = set(self.vertexSet)
        trace_sol = copy.deepcopy(self.trace)
        self.lock.release()
        return vertex_sol, trace_sol

from solution.networkXSol import NetworkXSol

"""
Generate another threads:
    - Monitor the time limit, and terminate solution thread
    - Running algorithm, and generate solution 
"""
def solutionExecutor(graph, solution, timeLimit, randomSeed, parameterDict, startTime):
    """
    graph = params_dict["graph"]
    solution = params_dict["solution"]
    time_limit = params_dict["timeLimit"]
    random_seed = params_dict["randomSeed"]
    parameter_dict = params_dict["parameterDict"]
    start_time = params_dict["startTime"]
    """

    print(solution)
    print(randomSeed)
    print(timeLimit)
    print(parameterDict)
    print(startTime)
    print(graph)

    # graph is a deep copy, thread-safe to change
    if solution == "BnB":
        pass
    elif solution == "LS1":
        pass
    elif solution == "LS2":
        pass
    elif solution == "Approx":
        pass
    elif solution == "NetworkX":
        pass
    else:
        print("Not Implemented Solution! Check Arguments!")
        raise RuntimeError

    solution = NetworkXSol(graph=graph, randomSeed=randomSeed, startTime=startTime, parameterDict=parameterDict)
    solution.updateVertexSet({1, 2, 3})
    solution.updateTrace(4)
    vertex_set, trace_list = solution.getSolution()

    # possible kill thread

    return vertex_set, trace_list
