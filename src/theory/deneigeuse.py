import numpy as np
from scipy import sparse

import utils

def discard_edge(G, i, j):
    G[i][j] = 0

def discard_node(G, i):
    for j in range(len(G)):
        discard_edge(G, i, j)
        discard_edge(G, j, i)

def discard_isolated_nodes(G, in_degree, out_degree):
    def rec_discard_isolated_node(i):
        if (in_degree[i] > 0) == (out_degree[i] > 0):
            return

        for j in range(len(G)):
            if G[i][j] > 0:
                G[i][j] = 0
                in_degree[j] -= 1
                rec_discard_isolated_node(j)
            elif G[j][i] > 0:
                G[j][i] = 0
                out_degree[j] -= 1
                rec_discard_isolated_node(j)

    for i in range(len(G)):
        rec_discard_isolated_node(i)

def get_degree_nodes_directed(G):
    n = len(G)
    in_degree = [0 for _ in range(n)]
    out_degree = [0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (G[i][j] > 0):
                out_degree[i] += 1
                in_degree[j] += 1

    return in_degree, out_degree

def compute_odd_pairs_directed(graph, in_degree, out_degree):

    odd_pairs = []
    for i in range(len(graph)):
        if in_degree[i] >= out_degree[i]:
            continue

        # noeuds avec surplus de edge sortant
        to_remove = out_degree[i] - in_degree[i]

        for j in range(len(graph)):
            if graph[i][j] == 0 or in_degree[j] <= out_degree[j]:
                continue

            # verifier si le voisin a un surplus de edge entrant
            discard_edge(graph, i, j)
            out_degree[i] -= 1
            in_degree[j] -= 1
            to_remove -= 1
            if to_remove == 0:
                break

    for i in range(len(graph)):
        if out_degree[i] >= in_degree[i]:
            continue

        for k in in_degree[i] - out_degree[i]:
            # find closest j with out_degree > in_degree

            # too much in edges
            # we need to add v outing edges
            # breadth first search starting from existsing outing edges
            pass

        pass

    return odd_pairs


def eulerize_graph(G):
    in_degree, out_degree = get_degree_nodes_directed(G)

    discard_isolated_nodes(G, in_degree, out_degree)

    odd_pairs, all_dist = compute_odd_pairs_directed(G, in_degree, out_degree)
    
    augmented_path = utils.create_augmented_path(G, odd_pairs, all_dist)

    # Add non-exist edge to G (Eulerize).
    # (However, we can only go through the edge. What if we have to pass more than 2 times ? counter instead of boolean may be better ?)
    G_aug = utils.deep_copy_with_mask(G)
    for u,v in augmented_path:
        G_aug[u][v] = (G_aug[u][v][0], True)

    return G_aug, augmented_path

def find_eulerian_circuit(G_aug, augmented_path, start):
    
    naive_circuit = []
    def find_eulerian_circuit_aux(G_aug, start):
        for i in range(len(G_aug)):
            
            if G_aug[start][i][0] > 0:
                if G_aug[start][i][1]: # Double edge
                    G_aug[start][i] = (G_aug[start][i][0], False)
                elif G_aug[i][start][1]:
                    G_aug[i][start] = (G_aug[i][start][0], False)
                else:                  # Only one edge
                    G_aug[start][i] = (0, False)
                    G_aug[i][start] = (0, False)
                find_eulerian_circuit_aux(G_aug, i)

        naive_circuit.append(start)

    find_eulerian_circuit_aux(G_aug, start)

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
