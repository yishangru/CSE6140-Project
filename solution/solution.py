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
        self.initialized = False
        self.vertexSet = set()
        # record trace
        self.startTime = startTime
        self.trace = list()

    def run(self):
        raise NotImplementedError

    def updateSolution(self, vertexSet):
        self.lock.acquire()
        if not self.initialized or len(self.vertexSet) > len(vertexSet):
            self.initialized = True
            self.__updateVertexSet(vertexSet)
            self.__updateTrace(len(vertexSet))
        self.lock.release()

    def getVCSize(self):
        return len(self.vertexSet)

    def getSolution(self):
        self.lock.acquire()
        vertex_sol = self.__getVertexSet()
        trace_sol = self.__getTrace()
        self.lock.release()
        return vertex_sol, trace_sol

    def __updateVertexSet(self, vertexSet):
        self.vertexSet = set(vertexSet)

    def __updateTrace(self, vertexSize):
        self.trace.append((format(time.time() - self.startTime, '.2f'), vertexSize))

    def __getVertexSet(self):
        return set(self.vertexSet)

    def __getTrace(self):
        return copy.deepcopy(self.trace)


"""
Main thread:
    - Monitor the time limit, and terminate solution thread
Generate another thread:   
    - Running algorithm, and generate solution 
"""


def solutionExecutor(graph, solution, timeLimit, randomSeed, parameterDict, startTime):

    from solution.networkXSol import NetworkXSol
    from solution.approxSol import ApproxSol, ApproxUpdateSol
    from solution.twSearchSol import TWSearchSol

    # graph is a deep copy, thread-safe to change
    solution_thread = NetworkXSol(graph=graph, randomSeed=randomSeed, startTime=startTime,
                                  parameterDict=parameterDict)
    if solution == "BnB":
        pass
    elif solution == "LS1":
        solution_thread = TWSearchSol(graph=graph, randomSeed=randomSeed, startTime=startTime,
                                      parameterDict=parameterDict)
    elif solution == "LS2":
        pass
    elif solution == "Approx":
        solution_thread = ApproxSol(graph=graph, randomSeed=randomSeed, startTime=startTime,
                                    parameterDict=parameterDict)
    elif solution == "ApproxUpdate":
        solution_thread = ApproxUpdateSol(graph=graph, randomSeed=randomSeed, startTime=startTime,
                                          parameterDict=parameterDict)
    elif solution == "NetworkX":
        solution_thread = NetworkXSol(graph=graph, randomSeed=randomSeed, startTime=startTime,
                                      parameterDict=parameterDict)
    else:
        print("Not Implemented Solution! Check Arguments!")
        raise RuntimeError

    solution_thread.start()
    solution_thread.join(timeout=timeLimit)

    vertex_set, trace_list = solution_thread.getSolution()

    # possible kill thread, still works without killing
    if solution_thread.is_alive():
        print("Warning: Thread is still alive! Return Solution.")

    return vertex_set, trace_list
