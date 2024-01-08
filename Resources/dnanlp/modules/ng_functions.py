#
# Network Graph Helper Functions
#
# The Python Quants GmbH
#
import pandas as pd
import networkx as nx
from pyvis.network import Network

def create_graph(data, labels=False):
    '''Create a NetworkX graph object from a pandas DataFrame.
    '''
    G = nx.DiGraph()
   
    vals = data[['Node1', 'Relation', 'Node2']].values
    G.add_edges_from([(v[0], v[2], {'relation': v[1]}) for v in vals])
   
    if labels:
        vals = data[['Label1', 'Node1', 'Label2', 'Node2']].values
        for v in vals:
            G.node[v[1]]['type'] = v[0]
            G.node[v[3]]['type'] = v[2]
    return G

def plot_graph(graph, background_color='white', 
               font_color='grey', with_edge_label=True,
               central_gravity=2.0, solver='',
               height='750px', width='100%', filter_=['']):
    ''' Creates a pyvis interactive Network Graph from a 
        NetworkX graph object.
    '''
    G = Network(notebook=True, height=height, width=width, 
                bgcolor=background_color, font_color=font_color)
    
    color = {0:'#fb217f', 1:'#fb217f', 2:'#88b1fb', 3:'#88b1fb', 4:'#88b1fb'}
    deg = dict(graph.in_degree())
    
    for node in graph:
        md = max(deg.values())
        color_id = min(deg[node], 4)
        G.add_node(node, title=node, label=node,
                   size=(md - deg[node] + 1) * 4,
                   color=color[color_id])
        
    for edge in graph.edges():
        if with_edge_label:
            label = graph.get_edge_data(edge[0], edge[1])['relation']
        else:
            label=''
        G.add_edge(edge[0], edge[1], label=label)
    if solver == 'barnes_hut':
        G.barnes_hut(central_gravity=central_gravity)
    else:
        G.force_atlas_2based(central_gravity=central_gravity)
    G.show_buttons(filter_=filter_)
    return G
