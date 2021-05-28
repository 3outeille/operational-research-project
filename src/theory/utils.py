class RegGraph:
    """
        Build regular graph representation from Osmnx graph.
    """
    
    def __init__(self, G, is_weighted=False):
        self.G = G
        self.is_weighted = is_weighted
        self.adjlist = self.create_adjlist(self.G)
        self.adjmat = self.adjlist_to_adjmat(self.adjlist)
        
    def create_adjlist(self, G):
        adjlist = []
        for src, nbrdict in self.G.adjacency():
            tmp = []
            for dst, w in nbrdict.items():
                if self.is_weighted:
                    tmp.append((dst, w['weight']))
                else:
                    tmp.append(dst)
            adjlist.append((src, tmp))
        return dict(adjlist)

    def adjlist_to_adjmat(self, adjlist):
        n = len(self.adjlist)
        adjmat = [[0 for j in range(n)] for i in range(n)]
        for src in range(n):
            if self.is_weighted:
                for dst, weight in self.adjlist[src]:
                    adjmat[src][dst] = weight
            else:
                for dst in self.adjlist[src]:
                    adjmat[src][dst] = 1
        return adjmat

    def pretty_print_adjmat(self):
        n = len(self.adjmat)

        print("  ",end="")
        for i in range(n):
            print("{} ".format(i), end="")

        print()

        for i in range(n):
            print("{} ".format(i), end="")
            for j in range(n):
                print(self.adjmat[i][j], end="|")
            print()

def create_random_graph(n, is_weighted=False):
    """
        Generating a random undirected weighted/unweighted graph.
    """
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        if is_weighted:
            w = random.randint(1, 100)
            E.add((*combination, w))
        else:
            E.add(combination)

    g = nx.Graph()
    g.add_nodes_from(V)
    
    if is_weighted:
        g.add_weighted_edges_from(E)
    else:
        g.add_edges_from(E)
        
    return g

def generate_and_save_graph():
    # Weighted
    for nb_node in [5, 10, 20]:
        G_weighted = create_random_graph(nb_node, is_weighted=True)
        graph_weighted = utils.RegGraph(G_weighted, is_weighted=True)

        adjmat = sp.sparse.csc_matrix(np.array(graph_weighted.adjmat))
        sp.sparse.save_npz("example/undirected_weighted_graph_{}.npz".format(nb_node), adjmat)
    
    # Unweighted
    for nb_node in [5, 10, 20]:
        G_unweighted = create_random_graph(nb_node, is_weighted=False)
        graph_unweighted = utils.RegGraph(G_unweighted, is_weighted=False)

        adjmat = sp.sparse.csc_matrix(np.array(graph_unweighted.adjmat))
        sp.sparse.save_npz("example/undirected_unweighted_graph_{}.npz".format(nb_node), adjmat)
