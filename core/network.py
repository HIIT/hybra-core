import networkx as nx
from matplotlib import pyplot as plt

import codecs
from string import Template

def create_network( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    G = nx.DiGraph()

    for node in data:
        G.add_node( node['creator'] )
        for comment in node['___comments']:
            G.add_edge( comment['from']['name'], node['creator'] )

    nx.draw_spring( G, with_labels = True , arrows = True )

def create_network_d3():
    html_template = Template( codecs.open('html/network.html', 'r').read() )

    css_text = codecs.open('css/network.css', 'r').read()
    js_text = codecs.open('js/network.js', 'r').read()

    return html_template.substitute( {'css': css_text, 'js': js_text} )

if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            create_network( data )
            plt.show()
