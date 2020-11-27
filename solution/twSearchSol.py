"""
This is a solution retrieved using local search Sol - Two Weighting Local Search.
"""
#------------ for mini test ------------#
import os, sys
sys.path.append("..")
sys.path.remove(os.path.abspath("."))
import time
from utils.data import readData
from main import optimalVC
#------------ for mini test ------------#

import random
from solution.solution import Solution


# greedy for initial solution - same as approximate
def greedy(graph):
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


# check whether a vertex set cover all edges, return uncovered edges, edgeWeight as dict[node1][node2] = weight
def checkCoverage(edgeWeight, vertexSet):
    uncovered_edge = list()
    for node in edgeWeight.keys():
        if node in vertexSet:
            continue
        for neighbor in edgeWeight[node].keys():
            if neighbor not in vertexSet:
                uncovered_edge.append((node, neighbor))
    return uncovered_edge


class TWSearchSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict
        # === Possible Move to Solution === #
        random.seed(randomSeed)

    # override parent method
    def run(self):
        # "Two weighting local search for minimum vertex cover."
        # Author: Cai, Shaowei, Jinkun Lin, and Kaile Su.
        # In Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 1107-1113. 2015.

        # parameter for two weight
        self.gamma, self.delta, self.beta = self.graph.edge//8, 10000, 0.8

        adjacent_matrix = self.graph.adjacent_matrix

        self.initialization()

        # === Possible Open Sub Thread for Greedy === #
        # get initial solution using approximate greedy
        self.current_solution = greedy(graph=self.graph)
        self.updateSolution(vertexSet=self.current_solution)

        self.step = 0
        self.restart = 0
        while self.getVCSize() > self.parameterDict["opt"]:
            uncover_edges = checkCoverage(self.edge_weights, self.current_solution)

            # choose a vertex for smaller search
            select_node = self.selectRemoveNode()

            # check whether new solution found
            if len(uncover_edges) == 0:
                print("Updating Solution At:" + str(self.step) + " , Len:" + str(len(self.current_solution)))
                self.restart = 0
                self.updateSolution(vertexSet=self.current_solution)
                self.removeNode(select_node)
                continue

            # add possible restart
            if self.restart > 0.25 * self.delta:
                print("Restart Solution ...")
                self.initialization()
                self.current_solution = self.getSolution()[0]
                self.restart = 0
                continue

            # try swap for another vertex
            self.removeNode(select_node)

            # update uncovered edges
            for neighbor in adjacent_matrix[select_node]:
                if neighbor not in self.current_solution:
                    assert neighbor != select_node, "run: node == neighbor"
                    if neighbor < select_node:
                        uncover_edges.append((neighbor, select_node))
                    elif neighbor > select_node:
                        uncover_edges.append((select_node, neighbor))

            # choose an uncovered edges randomly, add node to solution
            select_edge = uncover_edges[random.randrange(len(uncover_edges))]
            add_node = self.chooseAddNode(select_edge)
            self.addNode(add_node)

            # update uncovered edges
            update_uncover = list()
            for i in range(len(uncover_edges)):
                edge = uncover_edges[i]
                if edge[0] == add_node or edge[1] == add_node:
                    continue
                update_uncover.append(i)

            # update edge weights
            for i in update_uncover:
                self.edge_weights[uncover_edges[i][0]][uncover_edges[i][1]] += 1
            if self.step % self.gamma == 0:
                for node in self.edge_weights.keys():
                    for neighbor in self.edge_weights[node].keys():
                        if self.edge_weights[node][neighbor] > 1:
                            self.edge_weights[node][neighbor] -= 1

            # update vertex weights
            for node in self.vertex_weights.keys():
                if node not in self.current_solution:
                    self.vertex_weights[node] += 1
            if self.step % 100 == 0:
                # ==== log ==== #
                print("Step:" + str(self.step) + " , Remove:" + str(select_node) + " , Add:" + str(add_node) +
                      " , Uncover:" + str(len(uncover_edges)) + ", Current: " + str(self.getVCSize()))
                # ==== log ==== #
                for node in self.vertex_weights.keys():
                    if self.vertex_weights[node] > 1:
                        self.vertex_weights[node] -= 1

            self.step += 1
            self.restart += 1

        solution, trace = self.getSolution()
        print("Len Solution & Uncovered Edge:")
        print(len(solution))
        print(checkCoverage(self.edge_weights, solution))
        print("Trace:")
        print(trace)

    # initialization
    def initialization(self):
        adjacent_matrix = self.graph.adjacent_matrix

        # initialize vertex ages
        self.vertex_ages = dict()

        # initialize vertex configuration
        self.vertex_configurations = dict()
        for node in adjacent_matrix.keys():
            self.vertex_configurations[node] = dict()
            for neighbor in adjacent_matrix[node]:
                self.vertex_configurations[node][neighbor] = 0

        # initialize vertex weights
        self.vertex_weights = dict()
        for node in adjacent_matrix.keys():
            self.vertex_weights[node] = 0

        # initialize edge weights, reference [node1][node2], where node1 < node2
        self.edge_weights = dict()
        for node in adjacent_matrix.keys():
            self.edge_weights[node] = dict()
            for neighbor in adjacent_matrix[node]:
                if neighbor > node:
                    self.edge_weights[node][neighbor] = 1

    # select greatest score vertex
    def selectRemoveNode(self):
        adjacent_matrix = self.graph.adjacent_matrix

        # calculate current score
        node_select, smallest_lost = -1, float("inf")

        for node in self.current_solution:

            # calculate lost if remove
            increase_lost = 0
            for neighbor in adjacent_matrix[node]:
                if neighbor not in self.current_solution:
                    assert neighbor != node, "selectRemoveNode: node == neighbor"
                    if neighbor > node:
                        increase_lost += self.edge_weights[node][neighbor]
                    elif neighbor < node:
                        increase_lost += self.edge_weights[neighbor][node]

            if increase_lost < smallest_lost:
                node_select, smallest_lost = node, increase_lost
            elif abs(increase_lost - smallest_lost) < 0.000001:  # equal, check age
                assert node_select != -1, "Selected Node as -1"
                duration1 = self.vertex_ages[node] if node in self.vertex_ages.keys() else self.step
                duration2 = self.vertex_ages[node_select] if node_select in self.vertex_ages.keys() else self.step
                if duration1 < duration2:
                    node_select, smallest_lost = node, increase_lost

        return node_select

    # remove node from current solution
    def removeNode(self, removeNode):
        self.updateConfiguration(removeNode)
        self.current_solution.remove(removeNode)
        self.vertex_ages[removeNode] = self.step

    # add node to current solution
    def addNode(self, addNode):
        self.updateConfiguration(addNode)
        self.current_solution.add(addNode)

    # choose new vertex
    def chooseAddNode(self, selectEdge):
        adjacent_matrix = self.graph.adjacent_matrix

        # check configuration change
        def checkConfiguration(node, vertexConfiguration):
            for neighbor in vertexConfiguration[node].keys():
                if vertexConfiguration[node][neighbor] == 1:
                    return True
            return False

        node1, node2 = selectEdge[0], selectEdge[1]

        flag1 = checkConfiguration(node1, self.vertex_configurations)
        flag2 = checkConfiguration(node2, self.vertex_configurations)

        assert flag1 or flag2, "chooseAddNode: Both Nodes Configuration Not Changed"

        if not flag1:
            return node2
        if not flag2:
            return node1

        # both configuration changed
        if abs(self.vertex_weights[node1] - self.vertex_weights[node2]) > self.delta:
            node_select = node1 if self.vertex_weights[node1] > self.vertex_weights[node2] else node2
            self.vertex_weights[node_select] *= self.gamma
            return node_select

        def calculateScore(node, currentSolution, adjacentMatrix, edgeWeights):
            score = 0
            for neighbor in adjacentMatrix[node]:
                if neighbor not in currentSolution:
                    assert neighbor != node, "chooseAddNode: node == neighbor"
                    if neighbor > node:
                        score += edgeWeights[node][neighbor]
                    elif neighbor < node:
                        score += edgeWeights[neighbor][node]
            return score

        # calculate lost if add
        score1 = calculateScore(node1, self.current_solution, adjacent_matrix, self.edge_weights)
        score2 = calculateScore(node2, self.current_solution, adjacent_matrix, self.edge_weights)

        if score1 < score2:
            return node1
        elif abs(score1 - score2) < 0.000001:  # equal, check age
            duration1 = self.vertex_ages[node1] if node1 in self.vertex_ages.keys() else self.step
            duration2 = self.vertex_ages[node2] if node2 in self.vertex_ages.keys() else self.step
            return node1 if duration1 < duration2 else node2
        return node2

    def updateConfiguration(self, node):
        # update configuration
        for neighbor in self.vertex_configurations[node].keys():
            self.vertex_configurations[node][neighbor] = 0
            self.vertex_configurations[neighbor][node] = 1


def mini_test_ls(graphPath):
    graph = readData(graphPath)
    graph_instance = graphPath.split("/")[-1].split(".")[0]

    sol = TWSearchSol(graph=graph,
                      randomSeed=123,
                      startTime=time.time(),
                      parameterDict={"graph_name": graph_instance,
                                     "opt": optimalVC[graph_instance] if graph_instance in optimalVC.keys() else -1})
    sol.run()

dataDir = "../data/Data"
"""
graph_file_list = os.listdir(dataDir)
for graph in graph_file_list:
    split_name = graph.split(".")
    if len(split_name) == 2 and split_name[1] == "graph":
        print(graph)
        mini_test_ls(dataDir + "/" + graph)
"""
mini_test_ls(dataDir + "/" + "star.graph")
