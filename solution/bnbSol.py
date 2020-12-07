"""
This is a solution retrieved using Branch and Bound.
"""

import math
from solution.solution import Solution


class BnBSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        def add_node(stack, node, cover):
            state_dict = {
                "node": node,
                "state": 0,
                "cover": cover,
                "append": list()
            }
            stack.append(state_dict)

        adjacent_matrix = self.graph.adjacent_matrix

        self.optimal_cover_size = float("inf")

        self.edge_number_mapping = dict()
        for node in adjacent_matrix.keys():
            self.edge_number_mapping[node] = len(adjacent_matrix[node])

        current_sol, visit_stack = set(), list()
        start_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
        add_node(visit_stack, start_node, 0)

        while len(visit_stack) > 0:
            current_node_dict = visit_stack[-1]

            # restore state
            if current_node_dict["state"] == 2:
                self.restore(current_sol, current_node_dict["append"])
                # print(str(current_node_dict["cover"]) + " --- " + str(len(visit_stack)))
                visit_stack.pop(-1)
                continue

            # search include node
            if current_node_dict["state"] == 0:
                if current_node_dict["cover"] > self.graph.edge:
                    raise Exception

                if current_node_dict["cover"] == self.graph.edge:
                    print("Search End -- " + str(len(current_sol)))
                    if len(current_sol) < self.optimal_cover_size:
                        self.updateSolution(current_sol)
                        self.optimal_cover_size = self.getVCSize()
                        if self.optimal_cover_size == self.parameterDict["opt"]:
                            print("Find optimal!")
                            break
                    current_node_dict["state"] = 2
                    continue

                current_node_dict["state"] = 1
                lower_bound = self.calculate_lb(current_sol, current_node_dict["node"], current_node_dict["cover"], True)
                if lower_bound < self.optimal_cover_size:
                    current_node_dict["append"].append(current_node_dict["node"])
                    update_cover_edge = self.extend(current_sol, current_node_dict["append"], current_node_dict["cover"])
                    max_degree_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
                    add_node(visit_stack, max_degree_node, update_cover_edge)
                continue

            # search not include node
            if current_node_dict["state"] == 1:
                self.restore(current_sol, current_node_dict["append"])
                current_node_dict["append"].clear()

                current_node_dict["state"] = 2
                lower_bound = self.calculate_lb(current_sol, current_node_dict["node"], current_node_dict["cover"], False)
                if lower_bound < self.optimal_cover_size:
                    for neighbor in adjacent_matrix[current_node_dict["node"]]:
                        if neighbor not in current_sol:
                            current_node_dict["append"].append(neighbor)
                    update_cover_edge = self.extend(current_sol, current_node_dict["append"], current_node_dict["cover"])
                    max_degree_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
                    add_node(visit_stack, max_degree_node, update_cover_edge)
                continue

    def calculate_lb(self, current_sol, search_node, cover_edge, include):
        return len(current_sol) + math.ceil((self.graph.edge - cover_edge) / self.edge_number_mapping[search_node]) \
            if include else len(current_sol) + self.edge_number_mapping[search_node]

    def extend(self, current_sol, add_node_list, covered_edge):
        adjacent_matrix = self.graph.adjacent_matrix
        for node in add_node_list:
            for neighbor in adjacent_matrix[node]:
                if neighbor not in current_sol:
                    self.edge_number_mapping[neighbor] -= 1
            covered_edge += self.edge_number_mapping[node]
            self.edge_number_mapping[node] = 0
            current_sol.add(node)
        return covered_edge

    def restore(self, current_sol, add_node_list):
        adjacent_matrix = self.graph.adjacent_matrix
        for node in add_node_list:
            for neighbor in adjacent_matrix[node]:
                if neighbor not in current_sol:
                    self.edge_number_mapping[neighbor] += 1
                    self.edge_number_mapping[node] += 1
            current_sol.remove(node)
