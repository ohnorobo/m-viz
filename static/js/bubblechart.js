
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


function embiggen_nth_element(data, n){
  for (var index in data) {
    var pitch = data[index];
    var notes = pitch['values'];

    var n_size = notes[n]['size'];
    notes[n]['size'] = 10 * n_size;
  }

  //ensmallen prev notes?
}

var audioElement = document.getElementById('audio');
console.log(audioElement);
console.log(songData);
console.log(songData[0]['values'].length);

for (var n=0; n<songData[0]['values'].length; n++){
  embiggen_nth_element(songData, n);
}


