import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

ox.config(log_console=True, all_oneway=True)
# define a point at the corner of California St and Mason St in SF
location_point = (37.791427, -122.410018)

# create network from point, inside bounding box of N, S, E, W each 100m from point
MDG = ox.graph_from_point(location_point, dist=200, dist_type="bbox", network_type="drive")
# MDG = ox.graph_from_place("Montréal, QC, Canada", network_type="drive")
fig, ax = ox.plot_graph(MDG, node_color="white", node_size=100)
MDG = nx.convert_node_labels_to_integers(MDG) # Use label to deal with node id

# Save graph
ox.io.save_graphml(MDG, 'test.graphml')
# Load graph
MDG = ox.io.load_graphml('test.graphml', edge_dtypes={"oneway": str})

MG = ox.utils_graph.get_undirected(MDG) # MultiDiGraph -> MultiGraph
# Define node positions data structure (dict) for plotting
node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in MG.nodes(data=True)}
fig, ax = plt.subplots(figsize=(10,10))
nx.draw_networkx(MG, pos=node_positions, node_size=400,ax=ax)
plt.savefig("test.png")

def save_graph(MDG, filename):
    ox.io.save_graphml(MDG, filename)

def load_graph(filename):
    return ox.io.load_graphml(filename, edge_dtypes={"oneway": str})

