from collections import Counter
import matplotlib.pyplot as plt

def create_timeline( data ):
    date_series = Counter( sorted( map( lambda d: d['date'], data ) ) )

    plt.plot_date( x = date_series.keys(), y = date_series.values(), fmt = "r-" )
    plt.grid( True )
    plt.show()
