"""
Top level solution wrapper, provide data read, solution output
"""
import threading

class Solution(threading.Thread):
    @classmethod
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.lock = threading.Lock()
        self.vertexSet = set()  # current best vertex set solution

    @classmethod
    def run(self):
        raise NotImplementedError

    @classmethod
    def getVertexSet(self):
        self.lock.acquire()
        vertex_sol = set(self.vertexSet)
        self.lock.release()
        return vertex_sol

    @classmethod
    def updateVertexSet(self, vertexSet):
        self.lock.acquire()
        self.vertexSet = set(vertexSet)
        self.lock.release()


from solution.networkXSol import networkXSol

def solutionExecutor(graph, solution, timeLimit, parameterDict=None):
    if solution == "BB":
        pass
    solution = Solution(set())
    return solution.getVertexSet()