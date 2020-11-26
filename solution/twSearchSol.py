"""
This is a solution retrieved using local search Sol - Two Weighting Local Search.
"""
import os, sys
sys.path.append("..")
sys.path.remove(os.path.abspath("."))


from solution.solution import Solution


# greedy for initial solution
def greedy(graph):
    # Max Degree Greedy Algorithm
    # Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
    # vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
    vc = []
    adjacent_matrix = graph.adjacent_matrix

    current_edge = graph.edge
    while current_edge > 0:
        # update when remove node
        max_degree_node = max(adjacent_matrix.keys(), key=(lambda k: len(adjacent_matrix[k])))

        for neighbor in adjacent_matrix[max_degree_node]:
            adjacent_matrix[neighbor].remove(max_degree_node)
        current_edge -= len(adjacent_matrix[max_degree_node])
        adjacent_matrix.pop(max_degree_node)
        vc.append(max_degree_node)
    return vc


# check whether a vertex set cover all edges
def checkCoverage(graph, vertexSet):
    adjacent_matrix = graph.adjacent_matrix

    covered_edge = 0
    for vertex in vertexSet:
        covered_edge += len(adjacent_matrix[vertex])
        for neighbor in adjacent_matrix[vertex]:
            if (neighbor in vertexSet) and (neighbor > vertex):
                covered_edge -= 1
    return True if covered_edge == graph.edge else False


class TWSearchSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # "Two weighting local search for minimum vertex cover."
        # Author: Cai, Shaowei, Jinkun Lin, and Kaile Su.
        # In Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 1107-1113. 2015.

        step = 0
        # initialize edge weights and vertex weights

        # get initial solution using approximate greedy
        current_solution = greedy(graph=self.graph)
        self.updateSolution(vertexSet=current_solution)

        while self.getVCSize() > self.parameterDict["opt"]:
            print(checkCoverage(self.graph, current_solution))
            break


def mini_test_ls(graphPath):
    import time
    from utils.data import readData
    from main import optimalVC

    graph = readData(graphPath)
    graph_instance = graphPath.split("/")[-1].split(".")[0]

    sol = TWSearchSol(graph=graph,
                           randomSeed=0,
                           startTime=time.time(),
                           parameterDict={"graph_name": graph_instance, "opt": optimalVC[graph_instance]})
    sol.run()

mini_test_ls("../data/Data/jazz.graph")