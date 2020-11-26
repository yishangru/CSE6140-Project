"""
This is a solution retrieved using local search Sol - Two Weighting Local Search.
"""

from solution.solution import Solution

class TWLocalSearchSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    def greedy(self):
        # Max Degree Greedy Algorithm
        # Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
        # vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
        vc = []
        adjacent_matrix = self.graph.adjacent_matrix

        current_edge = self.graph.edge
        while current_edge > 0:
            # update when remove node
            max_degree_node = max(adjacent_matrix.keys(), key=(lambda k: len(adjacent_matrix[k])))

            for neighbor in adjacent_matrix[max_degree_node]:
                adjacent_matrix[neighbor].remove(max_degree_node)
            current_edge -= len(adjacent_matrix[max_degree_node])
            adjacent_matrix.pop(max_degree_node)
            vc.append(max_degree_node)
        return vc

    def checkCoverage(self):
        pass

    # override parent method
    def run(self):
        # "Two weighting local search for minimum vertex cover."
        # Author: Cai, Shaowei, Jinkun Lin, and Kaile Su.
        # In Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 1107-1113. 2015.

        step = 0
        # initialize edge weights and vertex weights

        # get initial solution using approximate greedy
        current_solution = self.greedy()
        self.updateSolution(vertexSet=current_solution)

        while self.getVCSize() > self.parameterDict["opt"]:
            pass

