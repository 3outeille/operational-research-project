import osmnx as ox
import networkx as nx
import numpy as np
import scipy as sp
from itertools import combinations
import random

import utils

def eulerize_graph(G):
    # CPP: Chinese Postman problem

    # CPP Step 1: Find Nodes of Odd Degree
    print(G)
    #nodes_odd_degree = [v for v, d in MG.degree() if d % 2 == 1]
    nodes_odd_degree = []

    for i, row in enumerate(G):
        degree = np.sum(np.where(row > 0, True, False))
        if degree % 2 == 1:
            nodes_odd_degree.append(i)

    print(nodes_odd_degree)

    # CPP Step 2: Find Min Distance Pairs
    # Step 2.1: Compute Node Pairs/Couple

    # Step 2.2: Compute Shortest Paths between Node Pairs/Couple

    # Step 2.3: Create Complete Graph

    # Step 2.4: Compute Minimum Weight Matching

    # Step 2.5: Augment the Original Graph

    return EG

def find_eulerian_circuit(adjmat, start):
    def find_eulerian_circuit_aux(circuit, adjmat, start):
        for i in range(len(adjmat)):
            if adjmat[start][i] > 0:
                adjmat[start][i] = 0
                adjmat[i][start] = 0
                find_eulerian_circuit_aux(circuit, adjmat, i)
        circuit.append(start)
        return circuit

    circuit = []
    return find_eulerian_circuit_aux(circuit, adjmat, start)

def print_circuit(circuit):
    for i, edge in enumerate(circuit):
        if i == 0:
            print(edge[0], end=" => ")
            print(edge[1], end="")
        else:
            print(end=" => ")
            print(edge[1], end="")
    print("\n")

def drone(filename):
    # Load graph
    G_sparse = sp.sparse.load_npz(filename)
    G = sp.sparse.csgraph.csgraph_to_dense(G_sparse)

    # Eulerize graph
    EG = eulerize_graph(G)

    # Find eulerian circuit
    circuit = find_eulerian_circuit(EG)

    # Print circuit
    print_circuit(circuit)


drone("example/undirected_unweighted_graph_5.npz")
