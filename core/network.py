import networkx as nx
import data_loader
from matplotlib import pyplot as plt

def create_network( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    G = nx.DiGraph()

    for node in data:
        G.add_node( node['creator'] )
        for comment in node['__comments']:
            G.add_edge( comment['from']['name'], node['creator'] )

    nx.draw_spring( G, with_labels = True , arrows = True )

if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            create_network( data )
            plt.show()
