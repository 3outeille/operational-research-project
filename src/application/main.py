import networkx as nx
import osmnx as ox
import pandas as pd

import solver

ox.config(log_console=True, all_oneway=True)

def main():
    # Graph initialization
    # define a point at the corner of California St and Mason St in SF
    location_point = (37.791427, -122.410018)

    # create network from point, inside bounding box of N, S, E, W each 100m from point
    # MDG = ox.graph_from_point(location_point, dist=175, dist_type="bbox", network_type="drive")

    # # Save graph
    # ox.io.save_graphml(MG, 'montreal-centreville-Graph.graphml')
    # Load graph
    MDG = ox.io.load_graphml('../theory/maps/montreal-graph.graphml', edge_dtypes={"oneway": str})
    # MDG = ox.io.load_graphml('../theory/maps/montreal-downtown-graph.graphml', edge_dtypes={"oneway": str})

    # create network from that bounding box
    #north, east = 45.512984, -73.553328
    #south, west = 45.496527, -73.581779
    #MDG = ox.graph_from_bbox(north, south, east, west, network_type="drive")
    MDG = nx.convert_node_labels_to_integers(MDG) # Use label to deal with node id
    MG = ox.utils_graph.get_undirected(MDG) # MultiDiGraph -> MultiGraph

    # Graph eulerization
    G_aug = solver.eulerize_graph(MG)

    # Find shortest circuit

    print(nx.is_eulerian(G_aug))

    print("find_shortest_circuit")
    euler_circuit = solver.find_shortest_circuit(G_aug, MG, start_node=0)

   # Print Circuit
    for i, edge in enumerate(euler_circuit):
        if i == 0:
            print(edge[0], end=" => ")
            print(edge[1], end="")
        else:
            print(end=" => ")
            print(edge[1], end="")

    print('\n')


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
    main()
