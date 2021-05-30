import numpy as np
from scipy import sparse

import utils

def get_odd_degree_nodes_directed(G):
    n = len(G)
    degree = [0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (G[i][j] > 0):
                degree[j] += 1
                degree[i] -= 1
    res = np.nonzero(degree)
    return res

def eulerize_graph(G):
    odd_degree_nodes = get_odd_degree_nodes_directed(G)
    odd_pairs, all_dist = utils.compute_odd_pairs(G, odd_degree_nodes)
    
    augmented_path = utils.create_augmented_path(G, odd_pairs, all_dist)

    # Add non-exist edge to G (Eulerize).
    # (However, we can only go through the edge. What if we have to pass more than 2 times ? counter instead of boolean may be better ?)
    G_aug = utils.deep_copy_with_mask(G)
    for u,v in augmented_path:
        G_aug[u][v] = (G_aug[u][v][0], True)

    return G_aug, augmented_path

def find_eulerian_circuit(G_aug, augmented_path, start):
    
    def find_eulerian_circuit_aux(naive_circuit, G_aug, start):
        for i in range(len(G_aug)):
            
            if G_aug[start][i][0] > 0:
                if G_aug[start][i][1]: # Double edge
                    G_aug[start][i] = (G_aug[start][i][0], False)
                elif G_aug[i][start][1]:
                    G_aug[i][start] = (G_aug[i][start][0], False)
                else:                  # Only one edge
                    G_aug[start][i] = (0, False)
                    G_aug[i][start] = (0, False)
                find_eulerian_circuit_aux(naive_circuit, G_aug, i)

        naive_circuit.append(start)
        return naive_circuit

    naive_circuit = []
    naive_circuit =  find_eulerian_circuit_aux(naive_circuit, G_aug, start)

    # Replace non-existing path with existing path.
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
                if (i == len(naive_circuit) - 2):
                    new_circuit.append(dst)
                is_already_present = False

    return naive_circuit, new_circuit

def run(filename):
    # Load graph
    G_sparse = sparse.load_npz(filename)
    G = sparse.csgraph.csgraph_to_dense(G_sparse)

    # Eulerize graph
    G_aug, augmented_path = eulerize_graph(G)
    
    # Find eulerian circuit
    naive_circuit, new_circuit = find_eulerian_circuit(G_aug, augmented_path, start=0)

    return naive_circuit, new_circuit
