"""
This is a solution retrieved using Branch and Bound.
"""
import sys
from solution.solution import Solution


class BnBSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        adjacent_matrix = self.graph.adjacent_matrix
        search_order = list(adjacent_matrix.keys())
        search_order.sort(key=lambda x: len(adjacent_matrix[x]), reverse=True)

        self.updateSolution(self.greedy())
        self.optimal_cover_size = self.getVCSize()
        sys.setrecursionlimit(max(self.optimal_cover_size + 1, 1500))

        # adjacent matrix will be updated
        pointer, current_sol = 0, set()
        self.search(pointer, current_sol, search_order, 0)

    # greedy for initial solution - same as approximate
    def greedy(self):
        # Max Degree Greedy Algorithm
        # Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
        # vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
        vc = set()
        adjacent_matrix = self.graph.adjacent_matrix
        current_edge = self.graph.edge

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

    def search(self, pointer, current_sol, search_order, covered_edge):

        if covered_edge > self.graph.edge:
            raise Exception
        if covered_edge == self.graph.edge:  # all is covered
            print("Search End -- " + str(len(current_sol)))
            if len(current_sol) < self.optimal_cover_size:
                self.updateSolution(current_sol)
                self.optimal_cover_size = self.getVCSize()
            return
        # no more search
        if pointer == len(search_order):
            return

        if search_order[pointer] in current_sol:
            self.search(pointer + 1, current_sol, search_order, covered_edge)
            return

        # include node
        lower_bound, update_cover_edge, add_list = self.extend(current_sol, search_order[pointer], covered_edge, True)
        if lower_bound < self.optimal_cover_size:
            # print("Add - " + str(pointer))
            self.search(pointer + 1, current_sol, search_order, update_cover_edge)
        for node in add_list:
            current_sol.remove(node)

        # not include node
        lower_bound, update_cover_edge, add_list = self.extend(current_sol, search_order[pointer], covered_edge, False)
        if lower_bound < self.optimal_cover_size:
            # print("Exclude - " + str(pointer))
            self.search(pointer + 1, current_sol, search_order, update_cover_edge)
        for node in add_list:
            current_sol.remove(node)

    def extend(self, current_sol, search_node, covered_edge, include):
        adjacent_matrix = self.graph.adjacent_matrix

        add_list = list()
        if include:
            lower_bound = len(current_sol) + 1
            if lower_bound < self.optimal_cover_size:
                covered_edge += len(adjacent_matrix[search_node])
                for neighbor in adjacent_matrix[search_node]:
                    if neighbor in current_sol:
                        covered_edge -= 1
                current_sol.add(search_node)
                add_list.append(search_node)
            return lower_bound, covered_edge, add_list

        # not include
        lower_bound = len(current_sol) + len(adjacent_matrix[search_node])
        for neighbor in adjacent_matrix[search_node]:
            if neighbor in current_sol:  # already covered
                lower_bound -= 1
        if lower_bound < self.optimal_cover_size:
            for neighbor in adjacent_matrix[search_node]:
                if neighbor not in current_sol:
                    covered_edge += len(adjacent_matrix[neighbor])
                    for node in adjacent_matrix[neighbor]:
                        if node in current_sol:
                            covered_edge -= 1
                    add_list.append(neighbor)
                current_sol.update(add_list)
        return lower_bound, covered_edge, add_list
