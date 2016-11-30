import networkx as nx

#from plotly.graph_objs import *

def create_network( data ):

    if len(data) == 0:
        print "Dataset empty."
        return nx.DiGraph()

    G = nx.DiGraph()

    for node in data:
        G.add_node( node['creator'] )
        for comment in node['__comments']:
            G.add_edge( comment['from']['name'], node['creator'] )

    nx.draw( G, with_labels = True , arrows = True)

    #pos = nx.fruchterman_reingold_layout( G )

    #edge_trace = scatter_edges( G, pos )
    #node_trace = scatter_nodes( pos, labels = pos.keys() )

    #network_data = Data( [edge_trace, node_trace] )
    #fig = Figure( data = network_data, layout = layout_settings() )

    #return fig


def scatter_nodes( pos, labels = None, color = None, size = 20, opacity = 1 ):
    trace = Scatter( x = [], y = [],  mode = 'markers', marker = Marker( size = [] ) )

    for node in pos:
        trace['x'].append( pos[node][0] )
        trace['y'].append( pos[node][1] )

    attrib = dict( name = '', text = labels , hoverinfo = 'text', opacity = opacity )
    trace = dict( trace, **attrib )
    trace['marker']['size'] = size
    return trace

def scatter_edges( G, pos, line_color = None, line_width = 1 ):
    trace = Scatter( x = [], y = [], mode = 'lines' )

    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0], pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1], pos[edge[1]][1], None]
        trace['hoverinfo'] = 'none'
        trace['line']['width'] = line_width
        if line_color is not None:
            trace['line']['color'] = line_color

    return trace

def axis_settings():
    return dict( showline = False,
                 zeroline = False,
                 showgrid = False,
                 showticklabels = False,
                 title = '' )

def layout_settings():
    axis = axis_settings()
    return Layout( xaxis = XAxis( axis ),
                   yaxis = YAxis( axis ),
                   hovermode = 'closest' )
