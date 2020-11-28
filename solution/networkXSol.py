"""
This is a solution retrieved using networkX.
"""

from solution.solution import Solution
import networkx as nx
from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover


class NetworkXSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # actual algorithm, update current best solution
        graph = nx.Graph()
        adjacent_matrix = self.graph.adjacent_matrix
        graph.add_nodes_from(list(adjacent_matrix.keys()))
        for node in adjacent_matrix.keys():
            for neighbor in adjacent_matrix[node]:
                if neighbor > node:
                    graph.add_edge(node, neighbor)

        mvc = min_weighted_vertex_cover(graph)
        print("NetworkX solution size: " + str(len(mvc)))
        self.updateSolution(mvc)
