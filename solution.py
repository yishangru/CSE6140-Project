"""
Top level solution wrapper, provide time limit, solution output
"""
from data import readData

class Solution(object):
    def __init__(self, graphName, timeLimit):
        self.graphName = graphName
        self.timeLimit = timeLimit

    def run(self):
        pass