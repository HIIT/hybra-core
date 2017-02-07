from __future__ import division, print_function
import os

path = os.path.dirname(os.path.abspath(__file__))

from collections import Counter
from datetime import date, timedelta
import codecs

from string import Template

def create_timeline(data):

    dates = map( lambda d: d['timestamp'].date(), filter( lambda d: d['timestamp'] is not '', data ) )

    y_axis = Counter( dates )

    start_date = min( y_axis )
    end_date = max( y_axis )
    delta = end_date - start_date

    x_axis = map( lambda date: start_date + timedelta( days = date ), range( delta.days + 1 ) )

    data_points = create_data_points( x_axis, y_axis )

    js_text_template = Template( codecs.open( path + '/js/timeline.js', 'r').read() )
    html_template = Template( codecs.open( path + '/html/timeline.html', 'r').read() )

    css_text = codecs.open( path + '/css/timeline.css', 'r').read()
    js_text = js_text_template.substitute({'data' : data_points})

    return html_template.substitute( {'css': css_text, 'js': js_text} )


def create_data_points( x_axis, y_axis ):
    data_points = []

    for date in x_axis:
        if date in y_axis:
            data_points.append({'close' : y_axis[date], 'date' : str(date)})
        else:
            data_points.append({'close' : 0, 'date' : str(date)})

    return data_points


if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print( function_name )
            f =  getattr( data_loader, function_name )
            data = f()
            create_timeline( data )
            plt.show()
