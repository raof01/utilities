"use restrict";

function plot(contents) {
  addRecords(contents);
  
  var data = {
    series: [
      getSeries()
    ]
  };

  var temp = getAvgSeries();
  var avgs = {
    labels: getAvgLabels(temp[0]),
    series: [
      {
        name: 'avgs', data: getAvgs(temp[0])
      },
      {
        name: 'all-avg', data: getAvgs(temp[1])
      }
    ]};
  
  new Chartist.Line(document.getElementById('data-plot'), data, {
    axisX: {
      type: Chartist.AutoScaleAxis,
      onlyInteger: true
    },lineSmooth: Chartist.Interpolation.none({
      fillHoles: false
    })
  }
                   );
  new Chartist.Line(document.getElementById('avgs-plot'), avgs, {
    series: {
      'avgs': {
        lineSmooth: Chartist.Interpolation.step()
      },
      'all-avg': {
        lineSmooth: Chartist.Interpolation.simple(),
      }
    },
    showPoint: false
  });
}