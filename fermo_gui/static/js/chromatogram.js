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
    // Extract sample data for plotting chromatogram lines
    var activeSampleData = statsChromatogram[sampleName];
    const traceInt = activeSampleData.map(obj => obj.trace_int);
    const traceRt = activeSampleData.map(obj => obj.trace_rt);

    // Extract sample data for tooltip
    const featureId = activeSampleData.map(obj => obj.f_id);
    const absInt = activeSampleData.map(obj => obj.abs_int);
    const relInt = activeSampleData.map(obj => obj.rel_int);
    const retTime = activeSampleData.map(obj => obj.rt);
    const precMz = activeSampleData.map(obj => obj.mz);

    // Get the max and min RT across all samples to use as plot range
    const allTraceRtValues = Object.values(statsChromatogram).
    flatMap(sample => sample.flatMap(obj => obj.trace_rt));
    const maxRt = Math.max(...allTraceRtValues);
    const minRt = Math.min(...allTraceRtValues);
    const upperRange = maxRt + maxRt * 0.02;
    const lowerRange = minRt - minRt * 0.05;

    // Fill or line colors of chromatogram peaks and legend
    var fillColors = ['#99bf9f', '#fce097'];
    var lineColors = ['#5a755e', '#fab80f'];
    var legendLabels = ['Selected', 'Blank'];

    // Data plotting
    var data = [];
    for ( var i = 0 ; i < traceRt.length ; i++ ) {

      var toolTip = `&nbsp;Feature ID: ${featureId[i]}<br>
                     Precursor m/z: ${precMz[i]}<br>
                     Retention time: ${retTime[i]}<br>
                     Relative intensity: ${relInt[i]}<br>
                     Absolute intensity: ${absInt[i]}<br>`

      var result = {
        showlegend: false,
        x: traceRt[i],
        y: traceInt[i],
        type: 'scatter',
        mode: 'lines',
        text: toolTip,
        hoverinfo: 'text',
        hoverlabel: { bgcolor: '#41454c' },
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

    // Legend layout
    for ( var i = 0 ; i < legendLabels.length ; i++ ) {
      var custom_legend = {
        x: [null],
        y: [null],
        mode: 'markers',
        name: legendLabels[i],
        marker: {
           size: 10,
           symbol: 'square',
           color: fillColors[i],
           line: {
              color: lineColors[i],
              width: 2
            }
        },
        showlegend: true
      };
      data.push(custom_legend);
    }

    // Axis layout
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