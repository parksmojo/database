from project5_classes.graph import Graph

tg = Graph(5)

def edges():
    # tg.mk_edge(0,1)
    # tg.mk_edge(0,2)
    # tg.mk_edge(1,0)
    # tg.mk_edge(2,1)
    # tg.mk_edge(2,2)
    # tg.mk_edge(4,3)
    # tg.mk_edge(4,4)

    tg.mk_edge(0,1)
    tg.mk_edge(0,2)
    tg.mk_edge(1,0)
    tg.mk_edge(1,2)
    tg.mk_edge(2,3)
    tg.mk_edge(2,4)
    tg.mk_edge(3,2)

    print(tg.to_string())

    tg.mk_reverse_graph()

    print(f"Dependency: {tg.dep_graph}")
    print(f"Reverse: {tg.rev_graph}")
    print(f"SCCs: {tg.find_sccs()}")

    # for i in range(len(self.datalog_program.rules)):
        #     print(f"[{i}] = {self.datalog_program.rules[i].to_string()}")
        # print(f"Dependency: {graph.dep_graph}")
        # print(f"Reverse: {graph.rev_graph}")
        # print(f"SCCs: {graph.find_sccs()}")

if __name__ == "__main__":
    edges()