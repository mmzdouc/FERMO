document.addEventListener('DOMContentLoaded', function() {
    // Load all chromatogram data
    var chromatogramElement = document.getElementById('mainChromatogram');
    var statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));

    // Automatically visualize the first sample on page load
    var firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        var firstSampleName = firstSample.getAttribute('data-sample-name');
        visualizeData(firstSampleName, statsChromatogram);
        document.getElementById('activeSample').textContent = 'Sample: ' + firstSampleName;
    }

    // Activate the clicked sample of the 'Sample overview'
    var rows = document.querySelectorAll('.select-sample');
    rows.forEach(function(row) {
       row.addEventListener('click', function() {
          var sampleName = this.getAttribute('data-sample-name');
          visualizeData(sampleName, statsChromatogram);
          document.getElementById('activeSample').textContent = 'Sample: ' + sampleName;
       });
    });
});

function visualizeData(sampleName, statsChromatogram) {
    // Extract sample data
    var activeSampleData = statsChromatogram[sampleName];
    const combinedTraceInt = activeSampleData.map(obj => obj.trace_int);
    const combinedTraceRt = activeSampleData.map(obj => obj.trace_rt);

    // Get the max and min RT across all samples to use as plot range
    const allTraceRtValues = Object.values(statsChromatogram).
    flatMap(sample => sample.flatMap(obj => obj.trace_rt));

    const maxRt = Math.max(...allTraceRtValues);
    const minRt = Math.min(...allTraceRtValues);
    const upperRange = maxRt + maxRt * 0.02;
    const lowerRange = minRt - minRt * 0.05;

    // TODO: add annotation for filtering or blank associated
    var colors = ['#6358f5'];
    var data = [];
    for ( var i = 0 ; i < combinedTraceRt.length ; i++ ) {
      var result = {
        showlegend: false,
        x: combinedTraceRt[i],
        y: combinedTraceInt[i],
        type: 'scatter',
        mode: 'lines',
        fill: 'toself',
        fillcolor: '#99bf9f',
        line: {
          color: '#5a755e',
          width: 2,
          shape: 'spline',
          smoothing: 0.8,
        }
      };
      data.push(result);
    }
    // TODO: make legends for other options
    var custom_legend = {
      x: [null],
      y: [null],
      mode: 'markers',
      name: 'Selected',
      marker: {
         size: 10,
         symbol: 'square',
         color: '#99bf9f',
         line: {
            color: '#5a755e',
            width: 2,
            shape: 'spline',
            smoothing: 0.8,
          }
      },
      showlegend: true
    };
    data.push(custom_legend);

    var layout = {
      height: 300,
      margin: { l: 50, r: 0, t: 0 },
      xaxis: {
        autorange: false,
        showgrid: false,
        visible: true,
        range: [lowerRange, upperRange]
      },
      yaxis: {
        autorange: false,
        showgrid: false,
        range: [0, 1.05],
        linecolor: 'black',
        zeroline: true,
        zerolinewidth: 0.5,
        zerolinecolor: 'black',
        title: 'Relative intensity',
        titlefont: {
          family: 'Arial',
          size: 12,
          color: 'grey'
        },
      },
    };
    Plotly.newPlot('mainChromatogram', data, layout);
}