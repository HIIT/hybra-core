from collections import Counter
from matplotlib import pyplot as plt
import datetime
import data_loader

def create_timeline( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    dates = map( lambda d: d['date'].date(), data )
    timeline_data = Counter( dates )

    x_axis = sorted( timeline_data )
    y_axis = []
    for date in x_axis:
        y_axis.append( timeline_data[date] )

    plt.plot_date( x = x_axis, y = y_axis, fmt = "r-" )
    ymin, ymax = plt.ylim()
    plt.ylim( 0, ymax + 1 )

if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            create_timeline( data )
            plt.show()
