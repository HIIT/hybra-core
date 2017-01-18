import networkx as nx
from networkx.readwrite import json_graph
import codecs
from string import Template

def create_network(data):

    G = nx.DiGraph()

    for node in data:
        G.add_node( node['creator'].encode('utf-8') )

        if '___comments' in node:
            for comment in node['___comments']:
                G.add_edge( comment['from']['name'].encode('utf-8'), node['creator'].encode('utf-8') )

    d = json_graph.node_link_data(G)

    html_template = Template( codecs.open('html/network.html', 'r').read() )

    js_template_type = 'svg' if len(d['nodes']) < 500 else 'canvas'
    js_text_template = Template( codecs.open('js/network_' + js_template_type +'.js', 'r').read() )

    css_text = codecs.open('css/network.css', 'r').read()
    js_text = js_text_template.substitute({'nodes' : d['nodes'], 'links' : d['links']})

    return html_template.substitute( {'css': css_text, 'js': js_text} )
