"""
Data reader for reading file and return generated adjacent graph in map.
For generated adjacent graph:
    key: nodeID, value: set(neighborNodeID_1, ..., neighborNodeID_m)
"""

import os


def readData(fileName):
    graphFile = open("data/DATA" + fileName, mode='r', encoding="utf-8")