from __future__ import division, print_function
import os
from collections import Counter
from datetime import datetime, date, timedelta
import time
from string import Template

path = os.path.dirname(os.path.abspath(__file__))

def create_timeline( datasets = [], colors = [] ):

    import codecs

    if not datasets: return "No data given to create timeline."

    plots = create_plots( datasets )

    graph_div_id = int( time.time() * 1000 )

    html_template = Template( codecs.open( path + '/timeline.html', 'r').read() )
    js_template = Template( codecs.open( path + '/timeline.js', 'r').read() )

    css_text = codecs.open( path + '/timeline.css', 'r').read()
    js_text = js_template.substitute( {'graph_div_id' : graph_div_id,
                                       'plots' : plots,
                                       'line_colors' : colors} )

    return html_template.substitute( {'graph_div_id': 'timeline_graph_' + str(graph_div_id),
                                      'css': css_text,
                                      'js': js_text} )


def create_plots( datasets ):
    plots = []

    for data in datasets:
        x_axis, y_axis = create_axes( data )
        plots.append( create_data_points( x_axis, y_axis ) )

    return plots


def create_axes( data ):
    dates_ok = filter( lambda d: d['timestamp'] > datetime(1970,1,1,0,10), data )
    dates = map( lambda d: d['timestamp'].date(), dates_ok )

    y_axis = Counter( dates )

    start_date = min( y_axis )
    end_date = max( y_axis )
    delta = end_date - start_date

    x_axis = map( lambda date: start_date + timedelta( days = date ), range( delta.days + 1 ) )

    return x_axis, y_axis


def create_data_points( x_axis, y_axis ):
    data_points = []

    for date in x_axis:
        if date in y_axis:
            data_points.append({'close' : y_axis[date], 'date' : str(date)})
        else:
            data_points.append({'close' : 0, 'date' : str(date)})

    return data_points
