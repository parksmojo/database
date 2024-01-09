from typing import Dict

class Graph:
    def __init__(self, size: int) -> None:
        self.dep_graph: Dict[int, set(int)] = {}
        self.rev_graph: Dict[int, set(int)] = {}
        self.visited: Dict[int, bool] = {}
        # self.post_order: list[int] = []

        for x in range(size):
            self.dep_graph[x] = set()
            self.rev_graph[x] = set()
            self.visited[x] = False

    def to_string(self) -> str:
        output_str: str = ""

        for x in self.dep_graph:
            output_str += f"R{x}:"
            sep = ""
            for y in self.dep_graph[x]:
                output_str += sep
                output_str += f"R{y}"
                sep = ","
            output_str += "\n"
        return output_str

    def mk_edge(self, parent: int, child: int) -> None:
        if parent in self.dep_graph:
            self.dep_graph[parent].add(child)
        else:
            self.dep_graph[parent] = {child}

    def visit_node(self, node: int) -> None:
        self.visited[node] = True

    def mk_reverse_graph(self) -> None:
        for parent in self.dep_graph:
            for child in self.dep_graph[parent]:
                if child in self.rev_graph:
                    self.rev_graph[child].add(parent)
                else:
                    self.rev_graph[child] = {parent}
        self.rev_graph = dict(sorted(self.rev_graph.items()))

    def find_postorder(self) -> list[int]:
        post_order: list[int] = []
        for node in self.visited:
            self.visited[node] = False
        for node in self.rev_graph:
            if self.visited[node] == False:
                post_order.extend(self.dfs_rev(node))
        # print(f"Post-order: {post_order}")
        return post_order
        
    def dfs_rev(self, curr_node: int) -> list[int]:
        nodes: list[int] = []
        self.visited[curr_node] = True
        for child in self.rev_graph[curr_node]:
            if not self.visited[child]:
                nodes.extend(self.dfs_rev(child))
        nodes.append(curr_node)
        return nodes
    
    def find_sccs(self) -> list[list[int]]:
        node_order: list[int] = self.find_postorder()
        node_order.reverse()
        sccs: list[list[int]] = []
        for node in self.visited:
            self.visited[node] = False
        for node in node_order:
            if self.visited[node] == False:
                sccs.append(self.dfs_dep(node))
        return sccs
    
    def dfs_dep(self, curr_node: int) -> list[int]:
        # print(f"curr_node = {curr_node}, with children: {self.dep_graph[curr_node]}")
        nodes: list[int] = []
        self.visited[curr_node] = True
        for child in self.dep_graph[curr_node]:
            if not self.visited[child]:
                nodes.extend(self.dfs_dep(child))
        nodes.append(curr_node)
        return nodes