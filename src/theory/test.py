import numpy as np
from scipy import sparse
import unittest

import drone
import deneigeuse


def total_distance(G, circuit):
    total = 0
    for i in range(len(circuit) - 1):
        src, dst = circuit[i], circuit[i + 1]
        total += G[src][dst]
    return total

def count_odd_degree(G):
    res = 0

    for i, row in enumerate(G):
        degree = np.sum(np.where(row > 0, True, False))
        if degree % 2 == 1:
            res += 1

    return res

def count_odd_degree_aug(G):
    res = 0
    for row in G:
        degree = 0
        for weight, is_double_edge in row:
            if weight > 0:
                degree += 1
            if is_double_edge:
                degree += 1
        res += 1 if (degree % 2 == 1) else 0
    return res

def is_all_edge_visited(G, circuit):
    G_visited = np.copy(G).astype(bool)

    for i in range(len(circuit) - 1):
        src, dst = circuit[i], circuit[i + 1]
        if G_visited[src][dst] and G_visited[dst][src]:
            G_visited[src][dst] = False
            G_visited[dst][src] = False

    return np.sum(G_visited) == 0

class TestDrone(unittest.TestCase):

    def test_undirected_weighted_graph_5(self):
        filename = "maps/undirected-weighted-graph-5.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        G_aug, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) < len(G), True)
        self.assertTrue(count_odd_degree_aug(G_aug) == 0, True)
        self.assertTrue(is_all_edge_visited(G, new_circuit), True)

    def test_undirected_unweighted_graph_5(self):
        filename = "maps/undirected-unweighted-graph-5.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        G_aug, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) < len(G), True)
        self.assertTrue(count_odd_degree_aug(G_aug) == 0, True)
        self.assertTrue(is_all_edge_visited(G, new_circuit), True)

    def test_undirected_unweighted_graph_10(self):
        filename = "maps/undirected-unweighted-graph-10.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        G_aug, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) < len(G), True)
        self.assertTrue(count_odd_degree_aug(G_aug) == 0, True)
        self.assertTrue(is_all_edge_visited(G, new_circuit), True)
    
    def test_undirected_unweighted_graph_20(self):
        filename = "maps/undirected-unweighted-graph-20.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        G_aug, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) < len(G), True)
        self.assertTrue(count_odd_degree_aug(G_aug) == 0, True)
        self.assertTrue(is_all_edge_visited(G, new_circuit), True)

class TestDeneigeuse(unittest.TestCase):

    def test_odd_degree(self):
        filename = "maps/directed-weighted-graph-10.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        odd_degree = deneigeuse.get_odd_degree_nodes_directed(G)

    def test_directed_unweighted_graph_20(self):
        filename = "maps/directed-unweighted-graph-20.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)


if __name__ == '__main__':
    unittest.main()
