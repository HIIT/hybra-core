import codecs
from string import Template

import os

import networkx as nx
from networkx.readwrite import json_graph


path = os.path.dirname(os.path.abspath(__file__))

def create_network(data):

    G = nx.DiGraph()

    for node in data:
        G.add_node( encode_utf8( node['creator'] ) )

        if '_comments' in node:
            for comment in node['_comments']:
                G.add_edge( encode_utf8( comment['from']['name'] ), encode_utf8( node['creator'] ) )

    d = json_graph.node_link_data(G)

    html_template = Template( codecs.open( path + '/html/network.html', 'r').read() )

    js_template_type = 'svg' if len(d['nodes']) < 500 else 'canvas'
    js_text_template = Template( codecs.open( path + '/js/network_' + js_template_type +'.js', 'r').read() )

    css_text = codecs.open( path + '/css/network.css', 'r').read()
    js_text = js_text_template.substitute({'nodes' : d['nodes'], 'links' : d['links']})

    return html_template.substitute( {'css': css_text, 'js': js_text} )

def encode_utf8( string ):
    try:
        return string.encode('utf8')
    except UnicodeDecodeError:
        return string
