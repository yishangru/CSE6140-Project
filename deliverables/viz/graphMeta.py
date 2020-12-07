import networkx as nx
import matplotlib.pyplot as plt
import random

import os, sys
sys.path.append("..")
sys.path.remove(os.path.abspath("."))

from utils.data import readData

graphDirectory = "../../data/Data"

sample_ratio_dict = {
    "delaunay_n10.graph": 0.5,
    "email.graph": 0.5,
    "netscience.graph": 0.5,
    "power.graph": 0.2,
    "hep-th.graph": 0.15,
    "as-22july06.graph": 0.1,
    "star.graph": 0.1,
    "star2.graph": 0.08,
}

layout_dict = {
    "delaunay_n10.graph": "kamada",
    "email.graph": "kamada",
    "power.graph": "fruchterman",
    "hep-th.graph": "fruchterman",
    "star.graph": "kamada",
    "star2.graph": "kamada",
    "as-22july06.graph": "fruchterman",
    "netscience.graph": "fruchterman"
}

def structureVisualization(graphName):
    graph = readData(os.path.join(graphDirectory, graphName))
    adjacent_matrix = graph.adjacent_matrix

    random.seed(123)

    graphNX = nx.DiGraph() if layout_dict[graphName] == "fruchterman" else nx.Graph()

    # sampling for better visualization effect
    sampled_nodes = set()
    for node in adjacent_matrix.keys():
        if random.random() < sample_ratio_dict[graphName]:
            sampled_nodes.add(node)

    graphNX.add_nodes_from(sampled_nodes)
    for node in sampled_nodes:
        for neighbor in adjacent_matrix[node]:
            if neighbor > node and neighbor in sampled_nodes:
                graphNX.add_edge(node, neighbor)

    options = {
        "node_size": 7,
        "node_color": ["#3288bd", "#99d594", "#fee08b", "#fc8d59", "#d53e4f"],
        "node_alpha": 1,
        "edge_width": 0.2,
        "edge_color": "black",
        "edge_alpha": 0.5,
    }

    # mapping extract from original graph
    graph_degree_list = [len(adjacent_matrix[node]) for node in graphNX]
    minDegree, maxDegree = min(graph_degree_list), max(graph_degree_list)

    # generate color mapping for edge
    def colorMapping(value):
        # mapping value to 0 - 1
        mapped_value = (value - minDegree) / (maxDegree - minDegree)
        return options["node_color"][round(mapped_value * (len(options["node_color"]) - 1))]

    pos_dict = {"spring": nx.spring_layout, "kamada": nx.kamada_kawai_layout, "fruchterman": nx.fruchterman_reingold_layout}

    pos = layout_dict[graphName]
    parameter = {"G": graphNX, "scale": 4}
    graph_pos = pos_dict[pos](**parameter)
    nx.draw_networkx_nodes(graphNX, graph_pos, node_size=options["node_size"],
                           alpha=options["node_alpha"], node_color=[colorMapping(len(adjacent_matrix[node])) for node in graphNX])
    nx.draw_networkx_edges(graphNX, graph_pos, width=options["edge_width"],
                           alpha=options["edge_alpha"], edge_color=options["edge_color"], arrows=False)

    graph_instance = graphName.split(".")[0]

    # show graph
    ax = plt.gca()
    ax.set_facecolor('#FFC1C1')
    plt.title(r"Structure Viz: $\bf{" + graph_instance + "}$")
    plt.savefig(graph_instance + "-" + pos + ".png", dpi=600, format='png', bbox_inches="tight")
    plt.show()


def main():
    graphCandidate = ["as-22july06.graph",
                      "delaunay_n10.graph",
                      "email.graph",
                      "hep-th.graph",
                      "power.graph",
                      "star.graph",
                      "star2.graph"]
    for graph_name in graphCandidate:
        structureVisualization(graph_name)
