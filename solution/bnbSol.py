"""
This is a solution retrieved using Branch and Bound.
"""

from solution.solution import Solution


class BnBSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        adjacent_matrix = self.graph.adjacent_matrix

        self.edge_number_mapping = dict()
        for node in adjacent_matrix.keys():
            self.edge_number_mapping[node] = len(adjacent_matrix[node])

        self.optimal_cover_size = float("inf")
        self.search()

    def search(self):
        cover_edge, current_sol = 0, set()

        def add_node(stack, node, cover):
            state_dict = {
                "node": node,
                "state": 0,
                "cover": cover,
            }
            stack.append(state_dict)

        visit_stack = list()
        start_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
        add_node(visit_stack, start_node, cover_edge)

        while len(visit_stack) > 0:
            current_node_dict = visit_stack[-1]

            # restore state
            if current_node_dict["state"] == 2:
                if "append" in current_node_dict.keys():
                    for node in current_node_dict["append"]:
                        self.restore(current_sol, node)
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
                    current_node_dict["state"] = 2
                    continue

                current_node_dict["state"] = 1
                lower_bound, add_list, update_cover_edge = self.calculate_lb(current_sol, current_node_dict["node"], current_node_dict["cover"], True)
                current_node_dict["append"] = add_list
                if lower_bound < self.optimal_cover_size:
                    max_degree_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
                    add_node(visit_stack, max_degree_node, update_cover_edge)
                continue

            # search not include node
            if current_node_dict["state"] == 1:
                for node in current_node_dict["append"]:
                    self.restore(current_sol, node)
                current_node_dict["state"] = 2
                lower_bound, add_list, update_cover_edge = self.calculate_lb(current_sol, current_node_dict["node"], current_node_dict["cover"], False)
                current_node_dict["append"] = add_list
                if lower_bound < self.optimal_cover_size:
                    max_degree_node = max(self.edge_number_mapping.keys(), key=(lambda k: self.edge_number_mapping[k]))
                    add_node(visit_stack, max_degree_node, update_cover_edge)
                continue

    def calculate_lb(self, current_sol, search_node, covered_edge, include):
        add_list = list()
        if include:
            lower_bound = len(current_sol) + 1
            if lower_bound < self.optimal_cover_size:
                add_list.append(search_node)
        else:
            adjacent_matrix = self.graph.adjacent_matrix
            lower_bound = len(current_sol) + self.edge_number_mapping[search_node]
            if lower_bound < self.optimal_cover_size:
                for neighbor in adjacent_matrix[search_node]:
                    if neighbor not in current_sol:
                        add_list.append(neighbor)

        for node in add_list:
            covered_edge = self.extend(current_sol, node, covered_edge)
        return lower_bound, add_list, covered_edge

    def extend(self, current_sol, search_node, covered_edge):
        adjacent_matrix = self.graph.adjacent_matrix
        for neighbor in adjacent_matrix[search_node]:
            if neighbor not in current_sol:
                self.edge_number_mapping[neighbor] -= 1
        covered_edge += self.edge_number_mapping[search_node]
        self.edge_number_mapping[search_node] = 0
        current_sol.add(search_node)
        return covered_edge

    def restore(self, current_sol, search_node):
        adjacent_matrix = self.graph.adjacent_matrix
        for neighbor in adjacent_matrix[search_node]:
            if neighbor not in current_sol:
                self.edge_number_mapping[neighbor] += 1
                self.edge_number_mapping[search_node] += 1
        current_sol.remove(search_node)
