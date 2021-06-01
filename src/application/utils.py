import networkx as nx


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
    """
    Add the min weight matching edges to the original graph
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list[tuples] of node pairs from min weight matching
    Returns:
        augmented NetworkX graph
    """

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
    """Create the eulerian path using only edges from the original graph."""
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
