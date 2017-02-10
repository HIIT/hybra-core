var width = 900,
    height = 600;

var color = d3.scale.category20();

var nodes = $nodes,
    links = $links;

var force = d3.layout.force()
    .size([width, height])
    .linkDistance(40)
    .charge(-120)
    .nodes(nodes)
    .links(links)
    .start();

var svg = d3.select('#network_graph_' + $graph_div_id).append('svg')
    .attr('width', width)
    .attr('height', height);

var link = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link");

var node = svg.selectAll(".node")
    .data(nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 8)
    .style("fill", function (d) {
      return color(d.group);
    })
    .call(force.drag)
    .on('dblclick', connectedNodes);

force.on("tick", function() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
});


var toggle = 0;

var linkedByIndex = {};
for (i = 0; i < nodes.length; i++) {
    linkedByIndex[i + "," + i] = 1;
};

links.forEach(function (d) {
    linkedByIndex[d.source.index + "," + d.target.index] = 1;
});

function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
}

function connectedNodes() {
    if (toggle == 0) {
        d = d3.select(this).node().__data__;
        node.style("opacity", function (o) {
            return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
        });

        link.style("opacity", function (o) {
            return d.index==o.source.index | d.index==o.target.index ? 1 : 0.1;
        });

        toggle = 1;

    } else {
        node.style("opacity", 1);
        link.style("opacity", 1);
        toggle = 0;
    }
}
