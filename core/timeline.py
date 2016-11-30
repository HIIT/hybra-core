from collections import Counter

#import plotly.graph_objs as go

def create_timeline( data ):

    if len(data) == 0:
        print "Dataset empty."
        return [go.Scatter( x = [] , y = [] )]

    timeline_data = Counter( sorted( map( lambda d: d['date'], data ) ) )
    return timeline_data

    #return [go.Scatter( x = date_series.keys() , y = date_series.values() )]
