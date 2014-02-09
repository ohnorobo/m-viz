nv.addGraph(function() {
   var chart = nv.models.scatterChart()
                 .showDistX(true)
                 .showDistY(true)
                 .color(d3.scale.category10().range());

   chart.xAxis.tickFormat(d3.format('.02f'))
   chart.yAxis.tickFormat(d3.format('.02f'))

   var data = getSongData()

   d3.select('#chart svg')
       .datum(data)
       .transition().duration(500)
       .call(chart);

   nv.utils.windowResize(chart.update);

   return chart;
 });


 function getSongData() { //# groups,# points per group
     return songData;
 }
