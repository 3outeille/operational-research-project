import numpy as np
from numpy.core.defchararray import count
from scipy import sparse

import utils

def get_odd_degree_nodes(G):
    odd_degree_nodes = []
    for i, row in enumerate(G):
        degree = np.sum(np.where(row > 0, True, False))
        if degree % 2 == 1:
            odd_degree_nodes.append(i)

    return odd_degree_nodes

def eulerize_graph(G):
    odd_degree_nodes = get_odd_degree_nodes(G)
    odd_pairs, all_dist = utils.compute_odd_pairs(G, odd_degree_nodes)
    
    augmented_path = utils.create_augmented_path(G, odd_pairs, all_dist)

    # Add non-exist edge to G (Eulerize).
    # (However, we can only go through the edge. What if we have to pass more than 2 times ? counter instead of boolean may be better ?)
    G_aug = utils.deep_copy_with_mask(G)

    for u,v in augmented_path:
        G_aug[u][v] = (G_aug[u][v][0], True)
        G_aug[v][u] = (G_aug[v][u][0], True)

    return G_aug, augmented_path
    
def find_eulerian_circuit(G_aug, augmented_path, start):

    def find_eulerian_circuit_aux(naive_circuit, G_aug, start):
        for i in range(len(G_aug)):

            if G_aug[start][i][0] > 0 or G_aug[start][i][1] == True:
                if G_aug[start][i][1]: # Double edge or edge doesn't exist
                    G_aug[start][i] = (G_aug[start][i][0], False)
                    G_aug[i][start] = (G_aug[i][start][0], False)
                else:                  # Only one edge
                    G_aug[start][i] = (0, False)
                    G_aug[i][start] = (0, False)
                find_eulerian_circuit_aux(naive_circuit, G_aug, i)

        naive_circuit.append(start)
        return naive_circuit

    naive_circuit = []
    G_aug_copy = [row[:] for row in G_aug] # Deep copy
    naive_circuit =  find_eulerian_circuit_aux(naive_circuit, G_aug_copy, start)

    # Replace non-existing path with existing path.
    naive_circuit = naive_circuit[::-1]
    new_circuit = []
    is_already_present = False
    for i in range(len(naive_circuit) - 1):
        src, dst = naive_circuit[i], naive_circuit[i + 1]

        if (src, dst) in augmented_path.keys():
            for e in augmented_path[(src, dst)]:
                new_circuit.append(e)
            is_already_present = True
        else:
            if not is_already_present:
                new_circuit.append(src)
            else:
                is_already_present = False

            if (i == len(naive_circuit) - 2):
                new_circuit.append(dst)

    return new_circuit

def run(filename):
    # Load graph
    G_sparse = sparse.load_npz(filename)
    G = sparse.csgraph.csgraph_to_dense(G_sparse)

    # Eulerize graph
    G_aug, augmented_path = eulerize_graph(G)

    # Find eulerian circuit
    new_circuit = find_eulerian_circuit(G_aug, augmented_path, start=0)
    
    return G_aug, new_circuit
