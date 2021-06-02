import osmnx as ox
import networkx as nx

def get_degree_nodes_directed(G):
    
    in_degree = [0 for _ in range(20000)]
    out_degree = [0 for _ in range(20000)]

    for (i, j) in G.edges():
        out_degree[i] += 1
        in_degree[j] += 1

    return in_degree, out_degree

def discard_isolated_nodes(G, in_degree, out_degree):
    def rec_discard_isolated_node(i):
        if not G.has_node(i) or (in_degree[i] > 0) == (out_degree[i] > 0):
            return

        edges = list(G.edges(i))

        G.remove_node(i)
        in_degree[i] = 0
        out_degree[i] = 0

        for src, dst in edges:
            if (src != i):

                out_degree[src] -= 1
                rec_discard_isolated_node(src)
            else:

                in_degree[dst] -= 1
                rec_discard_isolated_node(dst)

    nodes = list(G.nodes())

    for i in nodes:
        rec_discard_isolated_node(i)
    

def compute_odd_pairs_directed(graph, in_degree, out_degree):
    odd_pairs = []

    for i in graph.nodes():
        if out_degree[i] >= in_degree[i]:
            continue

        # {(0, 5): (0, 2, 4, 5)}

        for _, j in nx.bfs_edges(graph, i):
            if (in_degree[i] == out_degree[i]):
                break
            if out_degree[j] <= in_degree[j]:
                continue

            nb_edges = min(in_degree[i] - out_degree[i], out_degree[j] - in_degree[j])
            
            odd_pairs.append((i, j, nb_edges))
            in_degree[j] += nb_edges
            out_degree[i] += nb_edges

    return odd_pairs
    
def add_augmenting_path(graph, odd_pairs):
    for src, dst, nb_edges in odd_pairs:
        path_nodes = nx.shortest_path(graph, src, dst)
        path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))
        
        for edge in path_edges:
            attributes = graph.edges[(*edge, 0)]
            for _ in range(nb_edges):
                graph.add_edge(*edge, **attributes)
    
def eulerize_directed_graph(MDG):
    # Define node positions data structure (dict) for plotting
    # node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in MG.nodes(data=True)}

    # STEP 1
    # Retirer impasses et routes chiantes peu enneigées ==> OPTI
    # MDG = ox.simplification.simplify_graph(MDG)

    # STEP 2
    # Compute odd_nodes (return in_degree and out_degree)
    in_degree, out_degree = get_degree_nodes_directed(MDG)

    print(len(MDG.nodes()))
    discard_isolated_nodes(MDG, in_degree, out_degree)
    print(len(MDG.nodes()))

    in_degree, out_degree = get_degree_nodes_directed(MDG)


    for i in MDG.nodes():
        if ((in_degree[i] == 0) != (out_degree[i] == 0)):
            print(i)
            print(in_degree[i])
            print(out_degree[i])
            raise Exception("not simple")
    
    # Compute odd_pairs
    odd_pairs = compute_odd_pairs_directed(MDG, in_degree, out_degree)

    # STEP 3
    # Compute augmented graph : add all virtual edges
    add_augmenting_path(MDG, odd_pairs)

    # STEP 4
    print(nx.is_eulerian(MDG))

    eulerian_path = nx.algorithms.euler.eulerian_path(MDG)

    for i, (src, dst) in enumerate(eulerian_path):
        if i == 0:
            print(src, end=" => ")
            print(dst, end="")
        else:
            print(end=" => ")
            print(dst, end="")

    print("\n")

    

def main():
    MDG = ox.io.load_graphml('../theory/maps/montreal-digraph.graphml', edge_dtypes={"oneway": str})

    og_mileage = sum(nx.get_edge_attributes(MDG, 'length').values())

    eulerize_directed_graph(MDG)
    circuit_mileage = sum(nx.get_edge_attributes(MDG, 'length').values())
    
    print('Mileage of circuit: {0:.2f}'.format(circuit_mileage))
    print('Mileage on original trail map: {0:.2f}'.format(og_mileage))
    print('Mileage retracing edges: {0:.2f}'.format(circuit_mileage-og_mileage))
    print('Percent of mileage retraced: {0:.2f}%\n'.format((1-circuit_mileage/og_mileage)*-100))


    


if __name__ == '__main__':
    main()
