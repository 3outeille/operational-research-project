from logging import raiseExceptions
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import scipy as sp
from itertools import combinations
import random

import utils

def eulerize_graph(G):
    # CPP: Chinese Postman problem

    nodes_odd_degree = []

    for i, row in enumerate(G):
        degree = np.sum(np.where(row > 0, True, False))
        if degree % 2 == 1:
            nodes_odd_degree.append(i)

    odd_pairs, all_dist = utils.compute_odd_pairs(G, nodes_odd_degree)
    
    # Step 2.5: Augment the Original Graph
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

    return new_circuit

def drone(filename):
    # Load graph
    G_sparse = sp.sparse.load_npz(filename)
    G = sp.sparse.csgraph.csgraph_to_dense(G_sparse)

    # Eulerize graph
    G_aug, augmented_path = eulerize_graph(G)
    
    # Find eulerian circuit
    new_circuit = find_eulerian_circuit(G_aug, augmented_path, start=0)

    print(new_circuit)


drone("undirected-weighted-graph-5.npz")


"""
##############
#    DRAFT 
##############

all_dist[key][value]
                `-> (dict: all_shortest_path, predecessors: dict)


# Add non-exist edge to G
for u,v in augmented_path:
    if G_copy[u][v][0] == 0:
        G_copy[u][v] = (-all_dist[u][0][v], False) # set non-existing edge to negative
    else:
        G_copy[u][v] = (G_copy[u][v][0], True)

naive_circuit = find_euler_circuit(G) # [0, 1, 2, 0, 1, 3]

new_circuit = []

# Replace non-existing path with existing path.

for i in range(len(naive_circuit) - 1):
    pair = ([naive_circuit[i]], [naive_circuit[i + 1])
    if (G[pair[0]][pair[1]] < 0):
        new_circuit.append(**augmented_path[pair])
    else
        new_circuit.append(pair)

circuit = [(0, 3, 1), 2, (0, 3, 1), 3]
"""