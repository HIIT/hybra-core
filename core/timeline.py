from __future__ import division, print_function
import os

path = os.path.dirname(os.path.abspath(__file__))

from collections import Counter
from datetime import date, timedelta
import codecs
import time

from string import Template

def create_timeline( datasets = [], colors = [] ):

    if not datasets: return "No data given to create timeline."

    plots = create_plots( datasets )

    graph_div_id = int( time.time() * 1000 )

    html_template = create_html_template( graph_div_id )
    js_template = Template( codecs.open( path + '/js/timeline.js', 'r').read() )

    css_text = create_css_text()
    js_text = js_template.substitute( {'graph_div_id' : graph_div_id,
                                       'plots' : plots,
                                       'line_colors' : colors} )

    return html_template.substitute( {'css': css_text, 'js': js_text} )


def create_plots( datasets ):
    plots = []

    for data in datasets:
        x_axis, y_axis = create_axes( data )
        plots.append( create_data_points( x_axis, y_axis ) )

    return plots


def create_axes( data ):
    dates = map( lambda d: d['timestamp'].date(), filter( lambda d: d['timestamp'] is not '', data ) )

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


def create_html_template( graph_div_id ):

    html_template = Template('''
        <style> $css </style>
        <div id="timeline_graph_''' + str(graph_div_id) + '''"></div>
        <script> $js </script>
    ''')

    return html_template


def create_css_text():
    css_text = '''
        path {
            stroke-width: 2;
            fill: none;
        }

        .axis path, .axis line {
            fill: none;
            stroke: grey;
            stroke-width: 1;
            shape-rendering: crispEdges;
        }
    '''

    return css_text
