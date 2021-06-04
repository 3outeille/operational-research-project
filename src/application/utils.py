from ipyleaflet import *
from networkx.algorithms.planar_drawing import make_bi_connected
import random

def generate_visualization(map, MG, eulerian_path, nb_deneigeuses):
    print('Generate visualization...')
    res = [elt[0] for elt in eulerian_path]
    node_dict = dict(MG.nodes(data=True))
    locations = [[node_dict[node]['y'], node_dict[node]['x']] for node in res]

    center = (45.5581645,-73.6788509) # Location of Montreal


    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(nb_deneigeuses)]

    
    m = Map(center=center, zoom=10.5)

    for i in range(nb_deneigeuses):
        ant_path = AntPath(
                locations=locations[i * len(locations)//nb_deneigeuses : (i + 1) * len(locations)//nb_deneigeuses],
                dash_array=[1, 10],
                delay=500,
                color=colors[i],
                weight=1,
                pulse_color='#3f6fba'
            )

        m.add_layer(ant_path)
    
    m.layout.width = '50%'
    m.layout.height = '300px'
    

    filename = f"{map}_circuit.html"
    m.save(filename)
    
    print('Saved visualization at ./{}'.format(filename))
    
