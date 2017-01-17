from collections import Counter
from datetime import date, timedelta
import codecs
from string import Template

def create_timeline(data):

    dates = map( lambda d: d['timestamp'].date(), filter( lambda d: d['timestamp'] is not '', data ) )
    timeline_data = Counter( dates )

    start = min( timeline_data )
    end = max( timeline_data )
    delta = end - start

    x_axis = map( lambda date: start + timedelta( days = date ), range( delta.days + 1 ) )

    formatted_data = []
    for date in x_axis:
        if date in timeline_data:
            formatted_data.append({'close' : timeline_data[date], 'date' : str(date)})
        else:
            formatted_data.append({'close' : 0, 'date' : str(date)})

    css_text = codecs.open('css/timeline.css', 'r').read()

    js_text_template = Template( codecs.open('js/timeline.js', 'r').read() )

    html_template = Template( codecs.open('html/timeline.html', 'r').read() )

    js_text = js_text_template.substitute({'data' : formatted_data})

    return html_template.substitute( {'css': css_text, 'js': js_text} )


if __name__ == '__main__':

    import data_loader
    data = data_loader.load_facebook( ['nokkahuilu'] )

    create_timeline(data)

    #for function_name in dir( data_loader ):

        #if 'load_' in function_name:

            #print function_name
            #f =  getattr( data_loader, function_name )
            #data = f()
            #create_timeline( data )
            #plt.show()
