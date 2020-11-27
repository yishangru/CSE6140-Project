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
        self.coveredVerticesSet = set() # a set of covered(used) vertices
        self.coveredVerticesList = [] # a list of covered(used) vertices
        # self.globalBestVC = []
        self.myGraph = copy.deepcopy(self.graph) # this graph will be modified

    # override parent method
    def run(self):
        # Main loop here
        for _ in range(self.steps):
            current_edge = self.graph.edge
            # If there are remaining edges, then there are two actions:
            # 1. add an unused vertex with some probability
            # 2. remove an used vertex, then add an unused vertex (switch a pair of vertices)
            # Summary: With some probability we remove a vertex used. And we always add a random unused vertex
            if current_edge > 0:
                # with some probability we remove an covered vertex
                probToRemove = 0.2 * (1 - self.T)
                self.randomlyRemoveCoveredVertex(probToRemove)
                # we always add a random unsed vertex
                oldEdge = self.myGraph.edge
                added = self.randomlyAddUncoveredVertex(1)
                newEdge = self.myGraph.edge
                if newEdge == oldEdge:
                    # with probability (1-T) we don't want to do this
                    probWithT = random.uniform(0, 1)
                    if probWithT >= T:
                        self.removeCoveredVertex(added) # reverse the operation
                    # with probability T we keep this worse solution

            # If all edges are covered, two possible actions:
            # 1. Remove an used vertex
            # 2. Switch an used vertex with another (remove then add)
            # Summary: With some probability we add an vertex unused. But we always remove an used vertex.
            else:
                probToAdd = 0.15
                self.randomlyAddUncoveredVertex(probToAdd)
                # remove a vertex
                oldEdge = self.myGraph.edge
                removed = self.randomlyRemoveCoveredVertex(1)
                newEdge = self.myGraph.edge
                if newEdge > oldEdge:
                    # with probability (1-T) we don't want to do this
                    probWithT = random.uniform(0, 1)
                    if probWithT >= T:
                        self.addUncoveredVertex(removed) # reverse the operation
                    # with probability T we keep this worse solution

            T = T * self.alpha
            T = max(T, 0.005)

            # update globalMax here
            # ==== TODO ======

        vc = [pair[0] for pair in self.coveredVertices] # get the final vertexSet
        self.updateSolution(vertexSet=vc)

    def randomlyRemoveCoveredVertex(self, probToRemove):
        rand = random.uniform(0, 1)
        removed = None
        if rand < probToRemove and len(self.coveredVertices) > 0:
            # remove a vertex
            vertexToRemove = random.choice(self.coveredVerticesList)
            self.removeCoveredVertex(vertexToRemove)
            removed = vertexToRemove
        return removed


    def removeCoveredVertex(self, vertexToRemove):
        self.coveredVerticesList.remove(vertexToRemove)
        self.coveredVerticesSet.remove(vertexToRemove)
        neighborVertices = self.graph[vertexToRemove]
        # if a neighbor vertex is also covered, then remove this vertex won't uncover the particular edge
        for neighbor in neighborVertices:
            if neighbor not in self.coveredVerticesSet:
                self.myGraph.edge += 1
        self.myGraph.node += 1
        self.myGraph[vertexToRemove] = copy.deepcopy(neighborVertices)


    def randomlyAddUncoveredVertex(self, probToAdd):
        rand = random.uniform(0, 1)
        added = None
        if rand < probToAdd and self.myGraph.node > 0:
            # add a vertex
            vertexToAdd = random.choice(self.myGraph.keys())
            added = vertexToAdd
        return added


    def addUncoveredVertex(self, vertexToAdd):
        self.myGraph.remove(vertexToAdd)
        self.myGraph.node -= 1
        neighborVertices = self.myGraph[vertexToAdd]
        for neighbor in neighborVertices:
            if neighbor not in self.coveredVerticesSet:
                self.myGraph.edge -= 1
        self.coveredVerticesSet.add(vertexToAdd)
        self.coveredVerticesList.append(vertexToAdd)


    # def sigmoid(x):
    #     return 1 / (1 + math.exp(-x))



