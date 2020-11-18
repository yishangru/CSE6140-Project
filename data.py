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
    meta = graph_data[0].strip().split()
    node_count, edge_count = int(meta[0]), int(meta[1])

    graph_file.close()

    # check whether adjacent relation as expected
    for i in range(1, len(graph_data)):
        edge_info = [int(node) for node in graph_data[i].strip().split()]

        # skip isolated vertex
        if len(edge_info) == 0:
            continue

        for neighbor in edge_info:
            if neighbor < 1:
                print("Neighbor node < 1!" + " --- Node: " + str(i))
                return False
            if neighbor > node_count:
                print("Neighbor node > node count!" + " --- Node: " + str(i))
                return False
            if neighbor == i:
                print("Node link with itself!" + " --- Node: " + str(i))
                return False
        graph[i].update(edge_info)

    # check adjacent relation completeness
    for node in graph.keys():
        for neighbor in graph[node]:
            if neighbor not in graph.keys():
                print("Incomplete graph, neighbor missing!" + " --- Node: " + str(i) + ", Neighbor: " + str(neighbor))
                return False
            if node not in graph[neighbor]:
                print("Incomplete graph, edge missing!" + " --- Node: " + str(i) + ", Neighbor: " + str(neighbor))
                return False

    # check whether edge number as expected
    edge_sum = sum([len(graph[node]) for node in graph.keys()])
    if edge_sum != 2 * edge_count:
        print("Edge Number is " + ("smaller" if edge_sum < edge_count else "bigger") + " than expected!")
        return False

    # check whether node number as expected
    if node_count != len(graph):
        print("Warning: Actual node number is " + ("smaller" if len(graph) < node_count else "bigger") +
              " than expected! If smaller, there is possible isolated vertex!")

    return True

# read graph data
def readData(readPath):
    graph_file = open(readPath, mode='r', encoding="utf-8")
    graph = collections.defaultdict(lambda: set())

    graph_data = graph_file.readlines()
    meta = graph_data[0].strip().split()
    node_count, edge_count = int(meta[0]), int(meta[1])

    graph_file.close()

    for i in range(1, len(graph_data)):
        edge_info = [int(node) for node in graph_data[i].strip().split()]

        # skip isolated vertex
        if len(edge_info) == 0:
            continue
        graph[i].update(edge_info)

    # there is graph with isolated vertex, we subtract those from node_count
    return Graph(node=len(graph), edge=edge_count, adjacent_matrix=graph)

# check solution complete
def checkSol(readPath, vertexSet):
    graph = readData(readPath)
    adjacent_matrix = graph.adjacent_matrix
    for vertex in vertexSet:
        for neighbor in adjacent_matrix[vertex]:
            adjacent_matrix[neighbor].remove(vertex)
        adjacent_matrix.pop(vertex)
    left_edge = sum([len(adjacent_matrix[node]) for node in adjacent_matrix.keys()])
    if left_edge != 0:
        print("Solution is not correct! Not all edge is covered!")
        return False
    return True

# write solution vertex
def writeSol(writePath, vertexSet):
    # write solution file
    solution_file = open(writePath, mode='w', encoding="utf-8")
    solution_file.write(str(len(vertexSet)) + "\n")
    solution_file.write(",".join(vertexSet) + "\n")
    solution_file.close()

# write trace file
def writeTrace(writePath, traceList):
    # write trace file
    trace_file = open(writePath, mode='w', encoding="utf-8")
    # trace[0] as time, trace[1] as vertex set size
    for trace in traceList:
        trace_file.write(str(trace[0]) + ", " + str(trace[1]) + "\n")
    trace_file.close()
