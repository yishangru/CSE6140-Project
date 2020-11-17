"""
Data read:
    Read graph file and return generated adjacent graph in map.
    For generated graph:
    1. node: number of nodes
    2. edge: number of edges
    3. adjacent matrix (key, value) dict
        key: nodeID
        value: set(neighborNodeID_1, ..., neighborNodeID_m)

Solution output:
    Write current best vertex solution to file
"""

import collections

class Graph(object):
    def __init__(self, node, edge, adjacent_matrix):
        self.node = node
        self.edge = edge
        self.adjacent_matrix = adjacent_matrix

# check whether the graph is valid
def checkData(readPath):
    graph_file = open(readPath, mode='r', encoding="utf-8")
    graph = collections.defaultdict(lambda: set())

    graph_data = graph_file.readlines()
    meta = graph_data[0].strip().split(",")
    node_count, edge_count = int(meta[0]), int(meta[1])

    # check whether node number as expected
    if node_count != (len(graph_data) - 1):
        print("Node Number is " + ("smaller" if node_count < (len(graph_data) - 1) else "bigger") + " than expected!")
        return False
    # check whether adjacent relation as expected

    # check whether edge number as expected

    for i in range(1, len(graph_data)):
        graph[i].update([int(node) for node in graph_data[i].strip().split()])
    return True

# read graph data
def readData(readPath):
    graph_file = open(readPath, mode='r', encoding="utf-8")
    graph = collections.defaultdict(lambda: set())

    graph_data = graph_file.readlines()
    meta = graph_data[0].strip().split(",")
    node_count, edge_count = int(meta[0]), int(meta[1])
    for i in range(1, len(graph_data)):
        graph[i].update([int(node) for node in graph_data[i].strip().split()])
    return Graph(node=node_count, edge=edge_count, adjacent_matrix=graph)

def writeSol(writePath, vertexSet):
    solution_file = open(writePath, mode='w', encoding="utf-8")
