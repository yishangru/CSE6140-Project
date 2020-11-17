"""
This is a solution retrieved using networkX.
"""

from solution.solution import Solution

class networkXSol(Solution):
    def __init__(self, graph, parameterDict):
        super().__init__(graph)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # actual algorithm, update current best solution
        pass