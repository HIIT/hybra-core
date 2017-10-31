var plots = $plots;
var line_colors = $line_colors;


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


var y_max = 0;
var x_range = new Array(2);

// Find out plot ranges
plots.forEach(function(data) {

    // Format plot dates
    data.forEach(function(d) {
        d.date = new Date(d.date);
        d.close = +d.close;
    });

    var x_extent = d3.extent(data, function(d) { return d.date; });

    if (x_range[0] == null) {
      x_range[0] = x_extent[0];
      x_range[1] = x_extent[1];
    }

    if (x_range[0] > x_extent[0]) {
      x_range[0] = x_extent[0];
    }

    if (x_range[1] < x_extent[1]) {
      x_range[1] = x_extent[1];
    }

    var y_largest = d3.max(data, function(d) { return d.close; });
    if (y_max < y_largest) {
      y_max = y_largest;
    }

});


// Scale the plots and determine line colors
for (i = 0; i < plots.length; i++) {
    var data = plots[i];

    if (i < line_colors.length) {
      var color = line_colors[i];
    } else {
      var color = "steelblue";
    }

    // Scale the range of the data
    var y_range = [0, y_max];

    x.domain(x_range);
    y.domain(y_range);

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("stroke", color)
        .attr("d", valueline(data));
}


// Add the X Axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

// Add the Y Axis
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);
