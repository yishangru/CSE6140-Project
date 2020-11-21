"""
This is a solution retrieved using local search Sol.
"""

from solution.solution import Solution

class LocalSearch1Sol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # "Two weighting local search for minimum vertex cover."
        # Author: Cai, Shaowei, Jinkun Lin, and Kaile Su.
        # In Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 1107-1113. 2015.
        pass