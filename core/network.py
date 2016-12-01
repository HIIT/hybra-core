import networkx as nx

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
