"""
This is a solution retrieved using networkX.
"""

import time
from solution.solution import Solution

class NetworkXSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict
        print(self.lock)

    # override parent method
    def run(self):
        # actual algorithm, update current best solution
        self.updateVertexSet({1, 2, 3})
        self.updateTrace(4)
        time.sleep(1)

