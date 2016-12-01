from collections import Counter
from matplotlib import pyplot as plt

#import plotly.graph_objs as go

def create_timeline( data ):
    if len(data) == 0:
        print "Dataset empty."
        return [go.Scatter( x = [] , y = [] )]

    timeline_data = Counter( sorted( map( lambda d: d['date'], data ) ) )
    plt.plot_date( x = timeline_data.keys(), y = timeline_data.values(), fmt = "r-" )

    #return [go.Scatter( x = date_series.keys() , y = date_series.values() )]
