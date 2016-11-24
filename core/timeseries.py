import data_loader
from collections import Counter
import matplotlib.pyplot as plt

def create_timeseries( series = '' ):
    data = data_loader.load_facebook()

    date_series = Counter( sorted( map( lambda d: d['date'], data ) ) )

    plt.plot_date( x = date_series.keys(), y = date_series.values(), fmt = "r-" )
    plt.grid( True )
    plt.show()

if __name__ == '__main__':
    create_timeseries()
