import osmnx as ox
import networkx as nx

import scipy as sp


def get_degree_nodes_directed(G):

    in_degree = [0 for _ in range(20000)]
    out_degree = [0 for _ in range(20000)]

    for (i, j) in G.edges():
        out_degree[i] += 1
        in_degree[j] += 1

    return in_degree, out_degree


def discard_relou_edges(graph, in_degree, out_degree):

    for i in graph.nodes():
        if in_degree[i] >= out_degree[i]:
            continue

        # noeuds avec surplus de edge sortant
        to_remove = out_degree[i] - in_degree[i]

        out_edges = list(graph.out_edges(i, keys=True))

        for src, dst, key in out_edges:
            if in_degree[dst] <= out_degree[dst]:
                continue

            graph.remove_edge(src, dst, key)
            out_degree[src] -= 1
            in_degree[dst] -= 1
            to_remove -= 1
            if to_remove == 0:
                break


def compute_odd_pairs_directed(graph, in_degree, out_degree):
    odd_pairs = []

    for i in graph.nodes():
        if out_degree[i] >= in_degree[i]:
            continue

        for _, j in nx.bfs_edges(graph, i):
            if (in_degree[i] == out_degree[i]):
                break
            if out_degree[j] <= in_degree[j]:
                continue

            nb_edges = min(in_degree[i] - out_degree[i],
                           out_degree[j] - in_degree[j])

            odd_pairs.append((i, j, nb_edges))
            in_degree[j] += nb_edges
            out_degree[i] += nb_edges

    return odd_pairs


def compute_odd_pairs_directed_perfect(graph, in_degree, out_degree):
    starting_nodes = []
    ending_nodes = []
    for node in graph.nodes():
        diff = out_degree[node] - in_degree[node]
        for _ in range(diff):
            ending_nodes.append(node)
        for _ in range(-diff):
            starting_nodes.append(node)

    ending_nodes_dict = {}
    for index, node in enumerate(ending_nodes):
        if node in ending_nodes_dict:
            ending_nodes_dict[node].append(index)
        else:
            ending_nodes_dict[node] = [index]

    # Compute all dijkstras between starting & ending nodes
    dist = [[None] * len(ending_nodes) for _ in starting_nodes]

    for src_index, src_node in enumerate(starting_nodes):
        if src_index % 100 == 0:
            print('{0:.2f} %'.format(src_index * 100 / len(starting_nodes)))

        full_dist = nx.single_source_dijkstra_path_length(
            graph, src_node, weight=lambda u, v, d: d[0]['length'])

        for dst_node in full_dist.keys():
            if dst_node in ending_nodes_dict:
                for dst_index in ending_nodes_dict[dst_node]:
                    dist[src_index][dst_index] = full_dist[dst_node]

    print('Matching nodes...')
    matching = sp.optimize.linear_sum_assignment(dist)

    print('Matched.')

    odd_pairs = []

    for src_index, dst_index in zip(*matching):
        odd_pairs.append(
            (starting_nodes[src_index], ending_nodes[dst_index], 1))

    return odd_pairs


def add_augmenting_path(graph, odd_pairs):
    for src, dst, nb_edges in odd_pairs:
        path_nodes = nx.shortest_path(graph, src, dst)
        path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))

        for edge in path_edges:
            attributes = graph.get_edge_data(*edge)
            attributes = attributes[list(attributes.keys())[0]]
            for _ in range(nb_edges):
                graph.add_edge(*edge, **attributes)


def get_strongly_connected_component(MDG):
    strongly_connected_nodes = max(
        nx.strongly_connected_components(MDG), key=len)
    return MDG.subgraph(strongly_connected_nodes).copy()


def eulerize_directed_graph(MDG):
    # Define node positions data structure (dict) for plotting
    # node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in MG.nodes(data=True)}

    # STEP 1
    # Retirer impasses et routes chiantes peu enneigées ==> OPTI
    # discard_isolated_nodes(MDG, in_degree, out_degree)

    # STEP 2
    # Compute odd_nodes (return in_degree and out_degree)
    in_degree, out_degree = get_degree_nodes_directed(MDG)

    # Remove relou edges
    # discard_relou_edges(MDG, in_degree, out_degree)

    # print(nx.algorithms.components.is_strongly_connected(MDG))

    # Compute odd_pairs
    # odd_pairs = compute_odd_pairs_directed(MDG, in_degree, out_degree)
    odd_pairs = compute_odd_pairs_directed_perfect(MDG, in_degree, out_degree)

    # STEP 3
    # Compute augmented graph : add all virtual edges
    add_augmenting_path(MDG, odd_pairs)

    if not nx.is_eulerian(MDG):
        raise Exception("not eulerian")


def main():
    print('Loading graph...')
    MDG = ox.io.load_graphml(
        '../theory/maps/montreal-digraph.graphml', edge_dtypes={"oneway": str})
    # MDG = ox.io.load_graphml(
    #     '../theory/maps/montreal-downtown-digraph.graphml', edge_dtypes={"oneway": str})

    print('Graph loaded, getting largest connected component...')
    MDG = get_strongly_connected_component(MDG)

    map_length = sum(nx.get_edge_attributes(MDG, 'length').values())
    print('Map length: {0:.2f}'.format(map_length))

    print('Eulerization...')
    eulerize_directed_graph(MDG)

    print('Computing path...')
    eulerian_path = nx.algorithms.euler.eulerian_path(MDG)

    circuit_length = sum(nx.get_edge_attributes(MDG, 'length').values())

    print('Circuit length: {0:.2f}'.format(circuit_length))
    print('Retrace ratio: {0:.2f}\n'.format(circuit_length / map_length))


if __name__ == '__main__':
    main()
