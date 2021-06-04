import networkx as nx
from ipyleaflet import *


def generate_visualization(map, MG, eulerian_path):
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

    filename = f"{map}_circuit.html"
    m.save(filename)
    
    print('Saved visualization at ./{}'.format(filename))
    
