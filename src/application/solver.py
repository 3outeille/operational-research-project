import itertools
import networkx as nx
import pandas as pd

import utils

def eulerize_graph(MG):
    # Define node positions data structure (dict) for plotting
    # node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in MG.nodes(data=True)}

    print('nodes_odd_degree')
    # CPP: Chinese Postman problem

    # CPP Step 1: Find Nodes of Odd Degree
    nodes_odd_degree = [v for v, d in MG.degree() if d % 2 == 1]

    print(len(nodes_odd_degree))

    print("max_weight_matching")
    # Step 2.4: Compute Minimum Weight Matching
    odd_matching_dupes = utils.compute_odd_pairs(MG, nodes_odd_degree)
    # odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)
    odd_matching = list(pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes]))

    print("add_augmenting_path_to_graph")
    # Step 2.5: Augment the Original Graph
    G_aug = utils.add_augmenting_path_to_graph(MG, odd_matching)

    return G_aug

def find_shortest_circuit(G_aug, MG, start_node):
    return utils.create_eulerian_circuit(G_aug, MG, start_node)
