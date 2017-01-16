from collections import Counter
import datetime
import codecs
from string import Template

def create_timeline(data):

    dates = map( lambda d: str( d['timestamp'].date() ), filter( lambda d: d['timestamp'] is not '', data ) )
    timeline_data = Counter( dates )

    x_axis = sorted( timeline_data )
    formatted_data = []
    for date in x_axis:
        formatted_data.append({'close' : timeline_data[date], 'date' : date})

    css_text = codecs.open('css/timeline.css', 'r').read()

    js_text_template = Template( codecs.open('js/timeline.js', 'r').read() )

    html_template = Template( codecs.open('html/timeline.html', 'r').read() )

    js_text = js_text_template.substitute({'data' : formatted_data})

    return html_template.substitute( {'css': css_text, 'js': js_text} )


if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            create_timeline( data )
            plt.show()
