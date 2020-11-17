"""
Top level solution wrapper, infrastructure
"""
import threading

class Solution(threading.Thread):
    @classmethod
    def __init__(self, graph, randomSeed):
        super().__init__()
        self.graph = graph
        self.randomSeed = randomSeed
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

"""
Generate another threads:
    - Monitor the time limit, and terminate solution thread
    - Running algorithm, and generate solution 
"""
def solutionExecutor(**params_dict):
    graph = params_dict["graph"]
    solution = params_dict["solution"]
    time_limit = params_dict["timeLimit"]
    random_seed = params_dict["randomSeed"]
    parameter_dict = params_dict["parameterDict"]

    print(solution)
    print(random_seed)
    print(time_limit)
    print(parameter_dict)
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

    solution = Solution(set())
    return solution.getVertexSet()