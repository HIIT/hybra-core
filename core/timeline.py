from collections import Counter
import datetime
from IPython.core.display import HTML
from string import Template

def create_timeline(data):

    dates = map( lambda d: str(d['timestamp'].date()), data )
    timeline_data = Counter( dates )

    x_axis = sorted( timeline_data )
    formatted_data = []
    for date in x_axis:
        formatted_data.append({'close' : timeline_data[date], 'date' : date})

    css_text = '''

        #graph { font: 12px Arial;}

        path {
            stroke: steelblue;
            stroke-width: 2;
            fill: none;
        }

        .axis path,
        .axis line {
            fill: none;
            stroke: grey;
            stroke-width: 1;
            shape-rendering: crispEdges;
        }

    '''

    js_text_template = Template('''

        // Set the dimensions of the canvas / graph
        var margin = {top: 30, right: 20, bottom: 30, left: 50},
            width = 600 - margin.left - margin.right,
            height = 270 - margin.top - margin.bottom;

        // Set the ranges
        var x = d3.time.scale().range([0, width]);
        var y = d3.scale.linear().range([height, 0]);

        // Define the axes
        var xAxis = d3.svg.axis().scale(x)
            .orient("bottom").ticks(5);

        var yAxis = d3.svg.axis().scale(y)
            .orient("left").ticks(5);

        // Define the line
        var valueline = d3.svg.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.close); });

        // Adds the svg canvas
        var svg = d3.select("#graph")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top + ")");


        var data = $data;

        data.forEach(function(d) {
            d.date = new Date(d.date);
            d.close = +d.close;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.close; })]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data));

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

    ''')

    html_template = Template('''
        <style> $css </style>
        <div id="graph"></div>
        <script> $js </script>
    ''')

    js_text = js_text_template.substitute({'data' : formatted_data})

    return HTML(html_template.substitute({'css': css_text, 'js': js_text}))


if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            create_timeline( data )
            plt.show()
