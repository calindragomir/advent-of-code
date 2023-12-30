from collections import namedtuple
import networkx as nx

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

Component = namedtuple("Component", "name, connections")

def solve(lines):
    G = nx.Graph()
    for line in lines:
        parts = line.split(":")
        n = parts[0].strip()
        connections = [c.strip() for c in parts[1].split(" ") if c != ""]

        if not G.has_node(n):
            G.add_node(n)

        for conn in connections:
            if not G.has_node(conn):
                G.add_node(conn)
            G.add_edge(n, conn)

    cutset = nx.minimum_edge_cut(G)
    G.remove_edges_from(cutset)
    a, b = list(nx.connected_components(G))
    return len(a) * len(b)


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
