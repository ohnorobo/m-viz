nv.addGraph(function() {
   var chart = nv.models.scatterChart()
                 .showDistX(true)
                 .showDistY(true)
                 .color(d3.scale.category10().range());

   chart.xAxis.tickFormat(d3.format('.02f'))
   chart.yAxis.tickFormat(d3.format('.02f'))

   d3.select('#chart svg')
       .datum(songData())
     .transition().duration(500)
       .call(chart);

   nv.utils.windowResize(chart.update);

   return chart;
 });





 /**************************************
  * Simple test data generator
  */

 function songData() { //# groups,# points per group
     //data = {"c": [], "c#": [], "d": [], "d#": [], "e": [], "f": [],
     //        "f#", [], "g", [], "g#", [], "a", [], "a#", [], "b", []}

     data = []

     //note_order = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

     $.getJSON("../json/queen.json", function(d) {data = d})

     return data;
 }
