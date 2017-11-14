var width = 900,
    height = 600;

var color = d3.scale.category20();

var nodes = $nodes,
    links = $links;

var canvas = d3.select('#network_graph_' + $graph_div_id).append('canvas')
    .attr('width', width)
    .attr('height', height)
var context = canvas.node().getContext("2d");

var force = d3.layout.force()
    .size([width, height])
    .linkDistance(40)
    .charge(-120)
    .nodes(nodes)
    .links(links)
    .on("tick", tick)
    .start();

function tick() {
  context.clearRect(0, 0, width, height);

  // draw links
  context.strokeStyle = "#ccc";
  context.beginPath();
  links.forEach(function(d) {
    context.moveTo(d.source.x, d.source.y);
    context.lineTo(d.target.x, d.target.y);
  });
  context.stroke();

  // draw nodes
  context.fillStyle = "steelblue";
  context.beginPath();
  nodes.forEach(function(d) {
    context.moveTo(d.x, d.y);
    context.arc(d.x, d.y, 4.5, 0, 2 * Math.PI);
  });
  context.fill();
}
