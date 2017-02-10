import codecs
import time
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

    graph_div_id = int( time.time() * 1000 )

    html_template = create_html_template( graph_div_id )

    js_template_type = 'svg' if len(d['nodes']) < 500 else 'canvas'
    js_template = Template( codecs.open( path + '/js/network_' + js_template_type +'.js', 'r').read() )

    css_text = css_text = create_css_text()
    js_text = js_template.substitute( {'graph_div_id' : graph_div_id,
                                       'nodes' : d['nodes'],
                                       'links' : d['links']} )

    return html_template.substitute( {'css': css_text, 'js': js_text} )

def encode_utf8( string ):
    try:
        return string.encode('utf8')
    except UnicodeDecodeError:
        return string


def create_html_template( graph_div_id ):

    html_template = Template('''
        <style> $css </style>
        <div id="network_graph_''' + str(graph_div_id) + '''"></div>
        <script> $js </script>
    ''')

    return html_template


def create_css_text():
    css_text = '''
        .node {
            fill: #ccc;
            stroke: #fff;
            stroke-width: 1px;
        }

        .link {
            stroke: #777;
            stroke-width: 2px;
        }
    '''

    return css_text
