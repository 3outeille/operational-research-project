from ipyleaflet import *
import networkx as nx
import pandas as pd

import src.generate_maps as generate_maps
import utils

def eulerize_graph(MG):
    if (MG.order() < 500):
        return nx.algorithms.euler.eulerize(MG)
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

def run(map, iter):

    print('Loading graph...')

    if map  == "montreal_graph":
        MG = generate_maps.generate_montreal_graph()
    else:
        MG = generate_maps.generate_downtown_montreal_graph()
    
    MG = nx.convert_node_labels_to_integers(MG)

    map_length = sum(nx.get_edge_attributes(MG, 'length').values())
    print('Map length: {0:.2f}'.format(map_length))

    # Graph eulerization
    G_aug = eulerize_graph(MG)

    print("find_shortest_circuit")
    eulerian_path = find_shortest_circuit(G_aug, MG, start_node=0)

    circuit_length = sum(nx.get_edge_attributes(MG, 'length').values())
    print('Circuit length: {0:.2f}'.format(circuit_length))
    print('Retrace ratio: {0:.2f}\n'.format(circuit_length / map_length))

    print('Generate visualization...')
    res = [elt[0] for elt in eulerian_path]
    node_dict = dict(MG.nodes(data=True))
    locations = [[node_dict[node]['y'], node_dict[node]['x']] for node in res]

    center = (45.5581645,-73.6788509) # Location of Montreal

    ant_path = AntPath(
            locations=locations,
            dash_array=[1, 10],
            delay=500,
            color='#7590ba',
            weight=1,
            pulse_color='#3f6fba'
        )

    m = Map(center=center, zoom=10.5)
    m.layout.width = '50%'
    m.layout.height = '300px'
    m.add_layer(ant_path)
    m.save(f"{map}_circuit.html")