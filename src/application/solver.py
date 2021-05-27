import itertools
import networkx as nx
import pandas as pd

import utils

def eulerize_graph(MG):
    # Define node positions data structure (dict) for plotting
    node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in MG.nodes(data=True)}

    # CPP: Chinese Postman problem

    # CPP Step 1: Find Nodes of Odd Degree
    nodes_odd_degree = [v for v, d in MG.degree() if d % 2 == 1]

    # CPP Step 2: Find Min Distance Pairs
    # Step 2.1: Compute Node Pairs/Couple
    odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))

    # Step 2.2: Compute Shortest Paths between Node Pairs/Couple
    weight = lambda u, v, d: d[0]['length']
    odd_node_pairs_shortest_paths = utils.get_shortest_paths_distances(MG, odd_node_pairs, weight)

    # Step 2.3: Create Complete Graph
    g_odd_complete = utils.create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

    # Step 2.4: Compute Minimum Weight Matching
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)
    odd_matching = list(pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes]))

    # Step 2.5: Augment the Original Graph
    G_aug = utils.add_augmenting_path_to_graph(MG, odd_matching)

    return G_aug

def find_shortest_circuit(G_aug, MG, start_node):
    return utils.create_eulerian_circuit(G_aug, MG, start_node)
