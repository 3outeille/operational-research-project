from scipy import sparse

def get_shortest_path_distances(graph):
    all_dist = {}

    for node in range(len(graph)):
        dist_matrix, predecessors = sparse.csgraph.dijkstra(csgraph=graph, directed=False, indices=node, return_predecessors=True)
        
        dist = {}
        for i, shortest_path in enumerate(dist_matrix):
            dist[i] = shortest_path

        all_dist[node] = (dist, predecessors)
    
    return all_dist

def compute_odd_pairs(graph, odd_nodes):
    matched = set()
    not_matched = set(odd_nodes)
    all_dist = get_shortest_path_distances(graph)
    res = []

    for u in odd_nodes:
        if (u in matched):
            continue

        matched.add(u)
        not_matched.remove(u)

        min_dist = -1
        min_node = -1
        
        for v in not_matched:
            if (min_dist > all_dist[u][0][v] or min_dist == -1):
                min_node = v
                min_dist = all_dist[u][0][v]

        matched.add(min_node)
        not_matched.remove(min_node)

        res.append((u, min_node))

    return res, all_dist

def deep_copy_with_mask(G):
    G_copy = []
    for row in G:
        tmp = []
        for elt in row:
            tmp.append((elt, False))
        G_copy.append(tmp)
    return G_copy

def create_augmented_path(G, odd_pairs, all_dist):
    # augmented_path = {(0, 1): (0,3,1)}       
    augmented_path = {}

    for (src, dst) in odd_pairs:
        tmp = dst
        path = [tmp]
        while (src != tmp):
            tmp = all_dist[src][1][tmp]
            path.insert(0, tmp)

        augmented_path[(src, dst)] = path
        
    return augmented_path