"""
This is a solution retrieved using approximate Sol.
"""
import math
import random
import copy

from solution.solution import Solution

class SimulatedAnnealing(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict
        self.T = parameterDict["T"] # Temperature
        self.steps = parameterDict["steps"] # max #iteration
        self.alpha = parameterDict["alpha"] # cooling factor
        random.seed(randomSeed) # set seeds

        # useful stuff
        self.coveredVerticesSet = self.greedy(copy.deepcopy(self.graph)) # a list of covered(used) vertices
        self.coveredVerticesList = list(self.coveredVerticesSet)  # a set of covered(used) vertices
        self.globalBestVC = copy.deepcopy(self.coveredVerticesList)
        # self.myGraph = copy.deepcopy(self.graph) # this graph will be modified
        self.myGraph = self.initGraph() # this graph will be modified

    def run(self):
        # Main loop here
        for _ in range(self.steps):
            current_edge = self.myGraph.edge
            # print(current_edge)
            # If there are remaining edges, then there are two actions:
            # 1. add an unused vertex with some probability
            # 2. remove an used vertex, then add an unused vertex (switch a pair of vertices)
            # Summary: With some probability we remove a vertex used. And we always add a random unused vertex
            # Update: only do add in current version
            if current_edge > 0:
                # with some probability we remove an covered vertex
                # probToRemove = 0.2 * (1 - self.T)
                # self.randomlyRemoveCoveredVertex(probToRemove)
                # we always add a random unsed vertex
                oldEdge = self.myGraph.edge
                added = self.randomlyAddUncoveredVertex(1)
                newEdge = self.myGraph.edge
                if newEdge == oldEdge:
                    # with probability (1-T) we don't want to do this
                    probWithT = random.uniform(0, 1)
                    if probWithT >= self.T:
                        self.removeCoveredVertex(added) # reverse the operation
                    # with probability T we keep this worse solution

            # If all edges are covered, two possible actions:
            # 1. Remove an used vertex
            # 2. Switch an used vertex with another (remove then add)
            # Summary: With some probability we add an vertex unused. But we always remove an used vertex.
            # Update: only do remove in current version
            else:
                # probToAdd = 0.15
                # self.randomlyAddUncoveredVertex(probToAdd)
                # remove a vertex
                oldEdge = self.myGraph.edge
                removed = self.randomlyRemoveCoveredVertex(1)
                newEdge = self.myGraph.edge
                if newEdge > oldEdge:
                    # with probability (1-T) we don't want to do this
                    probWithT = random.uniform(0, 1)
                    if probWithT >= self.T:
                        self.addUncoveredVertex(removed) # reverse the operation
                    # with probability T we keep this worse solution

            self.T = self.T * self.alpha
            self.T = max(self.T, 0.005)


            # update globalMax here
            # ==== TODO ======
            if self.myGraph.edge == 0 and len(self.globalBestVC) == 0 or len(self.globalBestVC) > len(self.coveredVerticesList):
                self.globalBestVC = copy.deepcopy(self.coveredVerticesList)

        # vc = self.coveredVerticesList # get the final vertexSet
        self.updateSolution(vertexSet=self.globalBestVC)

    # # override parent method
    # def run(self):
    #     # Main loop here
    #     for _ in range(self.steps):
    #         current_edge = self.myGraph.edge
    #         # print(current_edge)
    #         # If there are remaining edges, then there are two actions:
    #         # 1. add an unused vertex with some probability
    #         # 2. remove an used vertex, then add an unused vertex (switch a pair of vertices)
    #         # Summary: With some probability we remove a vertex used. And we always add a random unused vertex
    #         # Update: only do add in current version
    #         if current_edge > 0:
    #             # with some probability we remove an covered vertex
    #             # probToRemove = 0.2 * (1 - self.T)
    #             # self.randomlyRemoveCoveredVertex(probToRemove)
    #             # we always add a random unsed vertex
    #             oldEdge = self.myGraph.edge
    #             added = self.randomlyAddUncoveredVertex(1)
    #             newEdge = self.myGraph.edge
    #             if newEdge == oldEdge:
    #                 # with probability (1-T) we don't want to do this
    #                 probWithT = random.uniform(0, 1)
    #                 if probWithT >= self.T:
    #                     self.removeCoveredVertex(added) # reverse the operation
    #                 # with probability T we keep this worse solution
    #
    #         # If all edges are covered, two possible actions:
    #         # 1. Remove an used vertex
    #         # 2. Switch an used vertex with another (remove then add)
    #         # Summary: With some probability we add an vertex unused. But we always remove an used vertex.
    #         # Update: only do remove in current version
    #         else:
    #             # probToAdd = 0.15
    #             # self.randomlyAddUncoveredVertex(probToAdd)
    #             # remove a vertex
    #             oldEdge = self.myGraph.edge
    #             removed = self.randomlyRemoveCoveredVertex(1)
    #             newEdge = self.myGraph.edge
    #             if newEdge > oldEdge:
    #                 # with probability (1-T) we don't want to do this
    #                 probWithT = random.uniform(0, 1)
    #                 if probWithT >= self.T:
    #                     self.addUncoveredVertex(removed) # reverse the operation
    #                 # with probability T we keep this worse solution
    #
    #         self.T = self.T * self.alpha
    #         self.T = max(self.T, 0.001)
    #
    #         # update globalMax here
    #         # ==== TODO ======
    #         if self.myGraph.edge == 0 and len(self.globalBestVC) == 0 or len(self.globalBestVC) > len(self.coveredVerticesList):
    #             self.globalBestVC = copy.deepcopy(self.coveredVerticesList)
    #
    #     # vc = self.coveredVerticesList # get the final vertexSet
    #     self.updateSolution(vertexSet=self.globalBestVC)

    def randomlyRemoveCoveredVertex(self, probToRemove):
        rand = random.uniform(0, 1)
        removed = None
        if rand < probToRemove and len(self.coveredVerticesList) > 0:
            # remove a vertex
            vertexToRemove = random.choice(self.coveredVerticesList)
            self.removeCoveredVertex(vertexToRemove)
            removed = vertexToRemove
        return removed


    def removeCoveredVertex(self, vertexToRemove):
        self.coveredVerticesList.remove(vertexToRemove)
        self.coveredVerticesSet.remove(vertexToRemove)
        neighborVertices = self.graph.adjacent_matrix[vertexToRemove]
        # if a neighbor vertex is also covered, then remove this vertex won't uncover the particular edge
        for neighbor in neighborVertices:
            if neighbor not in self.coveredVerticesSet:
                self.myGraph.edge += 1
        self.myGraph.node += 1
        self.myGraph.adjacent_matrix[vertexToRemove] = copy.deepcopy(neighborVertices)


    def randomlyAddUncoveredVertex(self, probToAdd):
        rand = random.uniform(0, 1)
        added = None
        if rand < probToAdd and self.myGraph.node > 0:
            # add a vertex
            vertexToAdd = random.choice(list(self.myGraph.adjacent_matrix.keys()))
            self.addUncoveredVertex(vertexToAdd)
            added = vertexToAdd
        return added


    def addUncoveredVertex(self, vertexToAdd):
        self.myGraph.adjacent_matrix.pop(vertexToAdd)
        self.myGraph.node -= 1
        neighborVertices = self.graph.adjacent_matrix[vertexToAdd]
        for neighbor in neighborVertices:
            if neighbor not in self.coveredVerticesSet:
                self.myGraph.edge -= 1
        self.coveredVerticesSet.add(vertexToAdd)
        self.coveredVerticesList.append(vertexToAdd)


    # greedy for initial solution - same as approximate
    def greedy(self, graph):
        # Max Degree Greedy Algorithm
        # Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
        # vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
        vc = set()
        adjacent_matrix = graph.adjacent_matrix
        current_edge = graph.edge

        edge_number_mapping = dict()
        for node in adjacent_matrix.keys():
            edge_number_mapping[node] = len(adjacent_matrix[node])

        while current_edge > 0:
            # update when remove node
            max_degree_node = max(edge_number_mapping.keys(), key=(lambda k: edge_number_mapping[k]))

            for neighbor in adjacent_matrix[max_degree_node]:
                if neighbor not in vc:
                    edge_number_mapping[neighbor] -= 1
            current_edge -= edge_number_mapping[max_degree_node]
            edge_number_mapping.pop(max_degree_node)
            vc.add(max_degree_node)
        return vc

    def initGraph(self):
        graph = copy.deepcopy(self.graph)
        graph.edge = 0 # initially all covered
        for vertex in self.graph.adjacent_matrix.keys():
            if vertex in self.coveredVerticesSet:
                graph.adjacent_matrix.pop(vertex)
                graph.node -= 1

        return graph


    # def sigmoid(x):
    #     return 1 / (1 + math.exp(-x))



