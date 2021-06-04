import networkx as nx
import pandas as pd

import src.generate_maps as generate_maps
import utils

def compute_odd_pairs(graph, odd_nodes):
    odd_nodes_set = set(odd_nodes)
    matched = set()
    res = []

    for i in odd_nodes:
        if i in matched:
            continue

        matched.add(i)

        for _, j in nx.bfs_edges(graph, i):
            if j in odd_nodes_set and j not in matched:

                matched.add(j)
                res.append((i, j))
                break

    return res

def add_augmenting_path_to_graph(graph, min_weight_pairs):
    # We need to make the augmented graph a MultiGraph so we can add parallel edges
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        graph_aug.add_edge(pair[0],
                           pair[1],
                           length=nx.dijkstra_path_length(
                               graph, pair[0], pair[1], weight="length"),
                           augmented=True
                           )
    return graph_aug


def create_eulerian_circuit(graph_augmented, graph_original, starting_node=None):
    euler_circuit = []
    naive_circuit = list(nx.eulerian_circuit(
        graph_augmented, source=starting_node))

    for edge in naive_circuit:
        edge_data = graph_augmented.get_edge_data(edge[0], edge[1])

        for k in edge_data.keys():
            if not 'augmented' in edge_data[k]:
                # If `edge` exists in original graph, grab the edge attributes and add to eulerian circuit.
                edge_att = graph_original[edge[0]][edge[1]]
                euler_circuit.append((edge[0], edge[1], edge_att))
                break
            else:
                aug_path = nx.shortest_path(graph_original, edge[0], edge[1], weight='length')
                aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))

                # If `edge` does not exist in original graph, find the shortest path between its nodes and
                #  add the edge attributes for each link in the shortest path.
                for edge_aug in aug_path_pairs:
                    edge_aug_att = graph_original[edge_aug[0]][edge_aug[1]]
                    euler_circuit.append(
                        (edge_aug[0], edge_aug[1], edge_aug_att))
                break
    return euler_circuit


def eulerize_graph(MG):
    if (MG.order() < 500):
        return nx.algorithms.euler.eulerize(MG)
  
    print('nodes_odd_degree')
    nodes_odd_degree = [v for v, d in MG.degree() if d % 2 == 1]

    print(len(nodes_odd_degree))

    print("max_weight_matching")
    odd_matching_dupes = compute_odd_pairs(MG, nodes_odd_degree)
    odd_matching = list(pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes]))

    print("add_augmenting_path_to_graph")
    G_aug = add_augmenting_path_to_graph(MG, odd_matching)

    return G_aug

def find_shortest_circuit(G_aug, MG, start_node):
    return create_eulerian_circuit(G_aug, MG, start_node)

def run(map):

    print('Downloading graph...')

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


    circuit_length = sum([edge[2][list(edge[2].keys())[0]]['length'] for edge in eulerian_path])

    print('Circuit length: {0:.2f}'.format(circuit_length))
    print('Retrace ratio: {0:.2f}\n'.format(circuit_length / map_length))

    utils.generate_visualization(map, MG, eulerian_path)