document.addEventListener('DOMContentLoaded', function() {
    // Load all chromatogram data
    var chromatogramElement = document.getElementById('mainChromatogram');
    var statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));

    // Automatically visualize the first sample on page load
    var firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        var firstSampleName = firstSample.getAttribute('data-sample-name');
        sampleData = getSampleData(firstSampleName, statsChromatogram)
        visualizeData(sampleData);
        document.getElementById('activeSample').textContent = 'Sample: ' + firstSampleName;

        // Update the feature table
        chromatogramElement.on('plotly_click', function(data) {
            var featureId = data.points[0].data.name;
            updateTableWithFeatureData(featureId, sampleData);
        });
    }

    // Activate the clicked sample of the 'Sample overview'
    var rows = document.querySelectorAll('.select-sample');
    rows.forEach(function(row) {
       row.addEventListener('click', function() {
          var sampleName = this.getAttribute('data-sample-name');
          sampleData = getSampleData(sampleName, statsChromatogram)
          visualizeData(sampleData);
          document.getElementById('activeSample').textContent = 'Sample: ' + sampleName;

          // Update the feature table
          chromatogramElement.on('plotly_click', function(data) {
              var featureId = data.points[0].data.name;
              updateTableWithFeatureData(featureId, sampleData);
          });
       });
    });

});

function visualizeData(sampleData) {
    var data = [];
    for ( var i = 0 ; i < sampleData.traceRt.length ; i++ ) {
      const { lineCol, fillCol } = getChromColors(sampleData, i)
      var result = {
        showlegend: false,
        x: sampleData.traceRt[i],
        y: sampleData.traceInt[i],
        type: 'scatter',
        mode: 'lines',
        name: `${sampleData.featureId[i]}`,
        text: getToolTip(sampleData, i),
        hoverinfo: 'text',
        hoverlabel: { bgcolor: '#41454c' },
        fill: 'toself',
        fillcolor: fillCol,
        line: {
          color: lineCol,
          width: 2,
          shape: 'spline',
          smoothing: 0.8,
        }
      };
      data.push(result);
    }

    // Legend layout
    const { legLab, lineCol, fillCol }  = getChromColors(sampleData, false)
    for ( var i = 0 ; i < legLab.length ; i++ ) {
      var custom_legend = {
        x: [null],
        y: [null],
        mode: 'markers',
        name: legLab[i],
        marker: {
           size: 10,
           symbol: 'square',
           color: fillCol[i],
           line: {
              color: lineCol[i],
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
        range: sampleData.upLowRange
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

function getSampleData(sampleName, statsChromatogram) {
    // Extract sample data for plotting chromatogram lines
    var activeSampleData = statsChromatogram[sampleName];

    // Get the max and min RT across all samples to use as plot range
    const allTraceRtValues = Object.values(statsChromatogram).
    flatMap(sample => sample.flatMap(obj => obj.trace_rt));
    const maxRt = Math.max(...allTraceRtValues);
    const minRt = Math.min(...allTraceRtValues);

    return {
        traceInt: activeSampleData.map(obj => obj.trace_int),
        traceRt: activeSampleData.map(obj => obj.trace_rt),
        featureId: activeSampleData.map(obj => obj.f_id),
        absInt: activeSampleData.map(obj => obj.abs_int),
        relInt: activeSampleData.map(obj => obj.rel_int),
        retTime: activeSampleData.map(obj => obj.rt),
        precMz: activeSampleData.map(obj => obj.mz),
        novScore: activeSampleData.map(obj => obj.novelty),
        blankAs: activeSampleData.map(obj => obj.blank),
        upLowRange: [minRt - minRt * 0.05, maxRt + maxRt * 0.02]
    }
}


function getChromColors(sampleData, peakNumber) {
    var fillColors = ['rgba(153, 191, 159, 0.70)', 'rgba(252, 224, 151, 0.70)'];
    var lineColors = ['#5a755e', '#fab80f'];
    var legendLabels = ['Selected', 'Blank'];

    if (peakNumber == false && peakNumber!== 0) {
        console.log(peakNumber)
        return { legLab: legendLabels, lineCol: lineColors, fillCol: fillColors };
    } else {
        switch (sampleData.blankAs[peakNumber]) {
        case true:
            return { lineCol: lineColors[1], fillCol: fillColors[1] };
        case false:
            return { lineCol: lineColors[0], fillCol: fillColors[0] };
        };
    };
}


function getToolTip(sampleData, peakNumber) {
    return `&nbsp;Feature ID: ${sampleData.featureId[peakNumber]}<br>
            Precursor m/z: ${sampleData.precMz[peakNumber]}<br>
            Retention time: ${sampleData.retTime[peakNumber]}<br>
            Relative intensity: ${sampleData.relInt[peakNumber]}<br>
            Absolute intensity: ${sampleData.absInt[peakNumber]}<br>`
}

function updateTableWithFeatureData(fId, sampleData) {
    // Update the general feature info table with the clicked feature data
    for ( var i = 0 ; i < sampleData.featureId.length ; i++ ) {
        if (sampleData.featureId[i] == fId) {
            document.getElementById('featureIdCell').textContent = sampleData.featureId[i];
            document.getElementById('precMzCell').textContent = sampleData.precMz[i];
            document.getElementById('retTimeCell').textContent = sampleData.retTime[i];
            document.getElementById('relIntCell').textContent = sampleData.relInt[i];
            document.getElementById('absIntCell').textContent = sampleData.absInt[i];
            document.getElementById('NovScore').textContent = sampleData.novScore[i];
            document.getElementById('BlankAs').textContent = sampleData.blankAs[i];
        }
    }
}