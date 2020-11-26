"""
This is a solution retrieved using approximate Sol.
"""

from solution.solution import Solution

class ApproxSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # Max Degree Greedy Algorithm
        # Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
        # vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
        vc = []
        adjacent_matrix = self.graph.adjacent_matrix
        degree_list = [(node, len(adjacent_matrix[node])) for node in adjacent_matrix.keys()]
        degree_list.sort(key=(lambda x: x[1]))

        current_edge = self.graph.edge
        max_idx = len(degree_list) - 1
        while current_edge > 0:
            # no update but just iteration
            max_degree_node = degree_list[max_idx][0]

            for neighbor in adjacent_matrix[max_degree_node]:
                adjacent_matrix[neighbor].remove(max_degree_node)
            current_edge -= len(adjacent_matrix[max_degree_node])
            adjacent_matrix.pop(max_degree_node)
            vc.append(max_degree_node)
            max_idx -= 1

        self.updateSolution(vertexSet=vc)


class ApproxUpdateSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
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

        self.updateSolution(vertexSet=vc)