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
    data = data_loader.load_facebook()
    create_network( data )
    plt.show()
