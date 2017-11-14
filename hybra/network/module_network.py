import os
import time
from string import Template

from IPython.core.display import HTML, display

path = os.path.dirname(os.path.abspath(__file__))

def create_network(data):

    import codecs
    import networkx as nx
    from networkx.readwrite import json_graph

    G = nx.DiGraph()

    for node in data:
        G.add_node( encode_utf8( node['creator'] ) )

        if '_comments' in node:
            for comment in node['_comments']:
                G.add_edge( encode_utf8( comment['from']['name'] ), encode_utf8( node['creator'] ) )

    d = json_graph.node_link_data(G)

    if not d['nodes']: return "Dataset empty."

    graph_div_id = int( time.time() * 1000 )

    html_template = Template( codecs.open( path + '/network.html', 'r').read() )

    js_template_type = 'svg' if len(d['nodes']) < 500 else 'canvas'
    js_template = Template( codecs.open( path + '/network_' + js_template_type +'.js', 'r').read() )

    css_text = codecs.open( path + '/network.css', 'r').read()

    js_text = js_template.substitute( {'graph_div_id' : graph_div_id,
                                       'nodes' : d['nodes'],
                                       'links' : d['links']} )

    html_template = html_template.substitute( {'graph_div_id': 'network_graph_' + str(graph_div_id),
                                      'css': css_text,
                                      'js': js_text} )

    display( HTML( html_template ) )

    return None

def encode_utf8( string ):
    try:
        return string.encode('utf8')
    except UnicodeDecodeError:
        return string
