import copy
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import pandas as pd

import utils

def solve():
    # define a point at the corner of California St and Mason St in SF
    location_point = (37.791427, -122.410018)

    # create network from point, inside bounding box of N, S, E, W each 100m from point
    MDG = ox.graph_from_point(location_point, dist=200, dist_type="bbox", network_type="drive")
    MDG = nx.convert_node_labels_to_integers(MDG) # Use label to deal with node id
    MG = ox.utils_graph.get_undirected(MDG) # MultiDiGraph -> MultiGraph

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
    g_aug = utils.add_augmenting_path_to_graph(MG, odd_matching)

    # CPP Step 3: Compute Eulerian Circuit
    euler_circuit = utils.create_eulerian_circuit(g_aug, MG, 0)

    # Print Circuit
    for i, edge in enumerate(euler_circuit):
        if i == 0:
            print(edge[0], end=" => ")
            print(edge[1], end="")
        else:
            print(end=" => ")
            print(edge[1], end="")

    # Compute statistics
    total_mileage_of_circuit = sum([edge[2][0]['length'] for edge in euler_circuit])
    total_mileage_on_orig_trail_map = sum(nx.get_edge_attributes(MG, 'length').values())
    _vcn = pd.value_counts(pd.value_counts([(e[0]) for e in euler_circuit]), sort=False)
    node_visits = pd.DataFrame({'n_visits': _vcn.index, 'n_nodes': _vcn.values})
    _vce = pd.value_counts(pd.value_counts([sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]))
    edge_visits = pd.DataFrame({'n_visits': _vce.index, 'n_edges': _vce.values})

# Printing stats
    print('Mileage of circuit: {0:.2f}'.format(total_mileage_of_circuit))
    print('Mileage on original trail map: {0:.2f}'.format(total_mileage_on_orig_trail_map))
    print('Mileage retracing edges: {0:.2f}'.format(total_mileage_of_circuit-total_mileage_on_orig_trail_map))
    print('Percent of mileage retraced: {0:.2f}%\n'.format((1-total_mileage_of_circuit/total_mileage_on_orig_trail_map)*-100))

    print('Number of edges in circuit: {}'.format(len(euler_circuit)))
    print('Number of edges in original graph: {}'.format(len(MG.edges())))
    print('Number of nodes in original graph: {}\n'.format(len(MG.nodes())))

    print('Number of edges traversed more than once: {}\n'.format(len(euler_circuit)-len(MG.edges())))

    print('Number of times visiting each node:')
    print(node_visits.to_string(index=False))

    print('\nNumber of times visiting each edge:')
    print(edge_visits.to_string(index=False))

if __name__ == '__main__':
    solve()
