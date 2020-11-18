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

    solution_thread = NetworkXSol(graph=graph, randomSeed=randomSeed, startTime=startTime, parameterDict=parameterDict)
    solution_thread.start()
    solution_thread.join(timeout=timeLimit)

    vertex_set, trace_list = solution_thread.getSolution()

    # possible kill thread, still works without killing
    if solution_thread.is_alive():
        print("Thread is still alive!")

    return vertex_set, trace_list
