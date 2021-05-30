from itertools import combinations
import networkx as nx
import numpy as np
import osmnx as ox
import random
import scipy as sp

###########################
#         UTILS
###########################

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

def add_edge(E, p, is_weighted, combi):
    a = random.random()
    if a < p:
        if is_weighted:
            w = random.randint(1, 100)
            E.add((*combi, w))
        else:
            E.add(combi)

def create_random_graph(n, p, is_weighted=False, is_directed=False):
    """
        Generating a random undirected weighted/unweighted graph.
    """
    V = set([v for v in range(n)])
    E = set()
    for combi in combinations(V, 2):
        add_edge(E, p, is_weighted, combi)
        if is_directed:
            add_edge(E, p, is_weighted, (combi[1], combi[0]))

    g = nx.DiGraph() if is_directed else nx.Graph()
    # g.add_nodes_from(V) # add_edges automatically adds nodes
    
    if is_weighted:
        g.add_weighted_edges_from(E)
    else:
        g.add_edges_from(E)
        
    return g

###########################
#         MAIN
###########################

def generate_random_graph(nb_node, p=0.5, is_weighted=False, is_directed=False):
    """
        Generating a random undirected weighted/unweighted graph.
    """
    G = create_random_graph(n=nb_node, p=p, is_weighted=is_weighted, is_directed=is_directed)
    G_reg = RegGraph(G, is_weighted=is_weighted)
    G = sp.sparse.csc_matrix(np.array(G_reg.adjmat))

    filename = "directed" if is_directed else "undirected"
    if is_weighted:
        sp.sparse.save_npz(filename + "-weighted-graph-{}.npz".format(nb_node), G)
    else:
        sp.sparse.save_npz(filename + "-unweighted-graph-{}.npz".format(nb_node), G)

def generate_montreal_graph():
    MDG = ox.graph_from_place("Montréal, QC, Canada", network_type="drive")
    MDG = nx.convert_node_labels_to_integers(MDG) # Use label to deal with node id
    MG = ox.utils_graph.get_undirected(MDG) # MultiDiGraph -> MultiGraph
    ox.io.save_graphml(MG, 'montreal-graph.graphml')

def generate_downtown_montreal_graph():
    # define a bounding box Centre-ville, Montréal, QC, Canada
    north, east = 45.512984, -73.553328
    south, west = 45.496527, -73.581779

    # create network from that bounding box
    MDG = ox.graph_from_bbox(north, south, east, west, network_type="drive")
    MDG = nx.convert_node_labels_to_integers(MDG) # Use label to deal with node id
    MG = ox.utils_graph.get_undirected(MDG) # MultiDiGraph -> MultiGraph
    ox.io.save_graphml(MG, 'montreal-downtown-graph.graphml')
    
ox.config(log_console=True, all_oneway=True)
#generate_montreal_graph()
#generate_downtown_montreal_graph()
generate_random_graph(nb_node=5, is_weighted=False, is_directed=True)
