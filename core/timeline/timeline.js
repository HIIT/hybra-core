// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 900 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

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
var svg = d3.select("#timeline_graph_" + $graph_div_id)
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

var plots = $plots;
var valueline_colors = $line_colors;

format_plot_dates(plots);
ranges = find_plot_ranges(plots);
create_plot_valuelines(plots, valueline_colors);
create_graph_axes(height);


function format_plot_dates(plots) {

    plots.forEach(function(data) {

        data.forEach(function(d) {
            d.date = new Date(d.date);
            d.close = +d.close;
        });
    });
}


function find_plot_ranges(plots) {
    var ranges = [];

    var x_range = new Array(2);
    var y_range = [0, 0];

    plots.forEach(function(data) {

        var x_extent = d3.extent(data, function(d) { return d.date; });

        if (x_range[0] == null) {
          x_range[0] = x_extent[0];
          x_range[1] = x_extent[1];
        } else if (x_range[0] > x_extent[0]) {
          x_range[0] = x_extent[0];
        } else if (x_range[1] < x_extent[1]) {
          x_range[1] = x_extent[1];
        }

        var y_largest = d3.max(data, function(d) { return d.close; });
        if (y_range[1] < y_largest) {
          y_range[1] = y_largest;
        }

    });

    ranges.push(x_range);
    ranges.push(y_range);

    return ranges;
}


function create_plot_valuelines(plots, valueline_colors) {
    for (i = 0; i < plots.length; i++) {
        var data = plots[i];

        var color = "steelblue";
        if (i < valueline_colors.length) { color = valueline_colors[i]; }

        x.domain(ranges[0]);
        y.domain(ranges[1]);

        svg.append("path")
            .attr("class", "line")
            .attr("stroke", color)
            .attr("d", valueline(data));
    }
}


function create_graph_axes(height) {
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
}
