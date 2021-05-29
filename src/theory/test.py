import numpy as np
from scipy import sparse
import unittest

import drone

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

class TestDrone(unittest.TestCase):

    def test_undirected_weighted_graph_5(self):
        filename = "maps/undirected-weighted-graph-5.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)

    def test_undirected_weighted_graph_10(self):
        filename = "maps/undirected-weighted-graph-10.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)
    
    def test_undirected_weighted_graph_20(self):
        filename = "maps/undirected-weighted-graph-20.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)

    def test_undirected_unweighted_graph_5(self):
        filename = "maps/undirected-unweighted-graph-5.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)

    def test_undirected_unweighted_graph_10(self):
        filename = "maps/undirected-unweighted-graph-10.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)
    
    def test_undirected_unweighted_graph_20(self):
        filename = "maps/undirected-unweighted-graph-20.npz"

        G_sparse = sparse.load_npz(filename)
        G = sparse.csgraph.csgraph_to_dense(G_sparse)
        naive_circuit, new_circuit = drone.run(filename)

        self.assertTrue(count_odd_degree(G) > 1, True)
        self.assertTrue(total_distance(G, new_circuit) <= total_distance(G, naive_circuit), True)

if __name__ == '__main__':
    unittest.main()