document.addEventListener('DOMContentLoaded', function() {
    // Load all chromatogram data
    var chromatogramElement = document.getElementById('mainChromatogram');
    var statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));

    // Automatically visualize the first sample on page load
    var firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        var firstSampleName = firstSample.getAttribute('data-sample-name');
        sampleData = getSampleData(firstSampleName, statsChromatogram)
        visualizeData(sampleData, false);
        document.getElementById('activeSample').textContent = 'Sample: ' + firstSampleName;

        // Update the feature table
        chromatogramElement.on('plotly_click', function(data) {
            var featureId = data.points[0].data.name;
            updateTableWithFeatureData(featureId, sampleData);
            addBoxVisualization(featureId, sampleData);
            var filteredSampleData = getFeatureData(featureId, sampleData);
            visualizeData(filteredSampleData, true);
        });
    }

    // Activate the clicked sample of the 'Sample overview'
    var rows = document.querySelectorAll('.select-sample');
    rows.forEach(function(row) {
       row.addEventListener('click', function() {
          var sampleName = this.getAttribute('data-sample-name');
          sampleData = getSampleData(sampleName, statsChromatogram)
          visualizeData(sampleData, false);
          document.getElementById('activeSample').textContent = 'Sample: ' + sampleName;
          Plotly.purge('featureChromatogram');

          // Update the feature table
          chromatogramElement.on('plotly_click', function(data) {
              var featureId = data.points[0].data.name;
              updateTableWithFeatureData(featureId, sampleData);
              addBoxVisualization(featureId, sampleData);
              var filteredSampleData = getFeatureData(featureId, sampleData);
              visualizeData(filteredSampleData, true);
          });
       });
    });
});


function visualizeData(sampleData, isFeatureVisualization = false) {
    var data = [];
    var maxPeaksPerSample = sampleData.traceInt.map(trace => Math.max(...trace));

    var combinedData = sampleData.traceRt.map((rt, i) => ({
        traceRt: rt,
        traceInt: sampleData.traceInt[i],
        featureId: sampleData.featureId[i],
        maxPeak: maxPeaksPerSample[i],
        chromColors: getChromColors(sampleData, i, isFeatureVisualization),
        toolTip: getToolTip(sampleData, i)
    }));

    combinedData.sort((a, b) => b.maxPeak - a.maxPeak);  // sort peaks so the smallest peaks are to the front

    // Create the Plotly data array
    combinedData.forEach(dataItem => {
        var result = {
            showlegend: false,
            x: dataItem.traceRt,
            y: dataItem.traceInt,
            type: 'scatter',
            mode: 'lines',
            name: `${dataItem.featureId}`,
            text: dataItem.toolTip,
            hoverinfo: 'text',
            hoverlabel: { bgcolor: '#41454c' },
            fill: 'toself',
            fillcolor: dataItem.chromColors.fillCol,
            line: {
                color: dataItem.chromColors.lineCol,
                width: 2,
                shape: 'spline',
                smoothing: 0.8,
            },
        };
        data.push(result);
    });

    // Legend layout
    const { legLab, lineCol, fillCol } = getChromColors(sampleData, false, isFeatureVisualization);
    for (var i = 0; i < legLab.length; i++) {
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

    // Add a custom legend item for a red dashed line if not feature visualization
    if (!isFeatureVisualization) {
        var redDashedLineLegend = {
            x: [null],
            y: [null],
            mode: 'markers',
            name: 'Selected feature',
            marker: {
                size: 8,
                symbol: 'line-ew',
                line: {
                    color: '#960303',
                    width: 2
                }
            },
            showlegend: true
        };
        data.push(redDashedLineLegend);
    }

    // Axis layout
    var layout = {
        height: isFeatureVisualization ? 150 : 300,
        margin: {
            l: 50, r: 0, t: 0,
            b: isFeatureVisualization ? 50 : 30,
            },
        xaxis: {
            autorange: false,
            showgrid: false,
            visible: true,
            range: sampleData.upLowRange,
            title: isFeatureVisualization ? 'Retention time (min)' : false,
            titlefont: isFeatureVisualization ? {
                family: 'Arial',
                size: 12,
                color: 'grey'
            } : false
        },
        yaxis: {
            autorange: false,
            showgrid: false,
            range: [0, 1.05],
            linecolor: 'black',
            zeroline: true,
            zerolinewidth: 0.5,
            zerolinecolor: 'black',
            title: isFeatureVisualization ? 'Rel. intensity' : 'Relative intensity',
            titlefont: {
                family: 'Arial',
                size: 12,
                color: 'grey'
            },
        },
    };

    // Choose the correct plot ID based on the visualization type
    var plotId = isFeatureVisualization ? 'featureChromatogram' : 'mainChromatogram';

    Plotly.newPlot(plotId, data, layout);
}


function getFeatureData(featureId, sampleData) {
    let filteredData = {
        featureId: [],
        fNetwork: [],
        traceInt: [],
        traceRt: [],
        precMz: [],
        retTime: [],
        relInt: [],
        absInt: [],
        upLowRange: [],
        blankAs: [],
        target: []
    };

    // Iterate through the original sampleData to find matching features
    for (var i = 0; i < sampleData.featureId.length; i++) {
        if (sampleData.featureId[i] == featureId) {
            filteredData.upLowRange.push(sampleData.upLowRange[0], sampleData.upLowRange[1]);
            filteredData.fNetwork.push(sampleData.fNetwork[i]);

            // Iterate through the fNetwork array to find the corresponding features
            for (var j = 0; j < sampleData.fNetwork[i].length; j++) {
                let key = sampleData.fNetwork[i][j];
                let index = sampleData.featureId.indexOf(key);

                if (index >= 0 && index < sampleData.traceInt.length) {
                    if (sampleData.featureId[index] == featureId) {
                        filteredData.target.push('selected');
                    } else {
                        filteredData.target.push('related');
                    }
                    filteredData.featureId.push(sampleData.featureId[index]);
                    filteredData.traceInt.push(sampleData.traceInt[index]);
                    filteredData.traceRt.push(sampleData.traceRt[index]);
                    filteredData.blankAs.push(sampleData.blankAs[index]);
                    filteredData.precMz.push(sampleData.precMz[index]);
                    filteredData.retTime.push(sampleData.retTime[index]);
                    filteredData.absInt.push(sampleData.absInt[index]);
                    filteredData.relInt.push(sampleData.relInt[index]);
                }
            }
        }
    }
    return filteredData;
}



function addBoxVisualization(featureId, sampleData) {
    var boxSizeX = 0.12;
    var boxSizeY = 0.04;

    for ( var i = 0 ; i < sampleData.featureId.length ; i++ ) {
        if (sampleData.featureId[i] == featureId) {
            var maxInt = Math.max(...sampleData.traceInt[i]);
            var maxRt = Math.max(...sampleData.traceRt[i]);
            var minRt = Math.min(...sampleData.traceRt[i]);
        };
    };

    var update = {
        shapes: [{
            type: 'rect',
            mode: 'lines',
            xref: 'x',
            yref: 'y',
            x0: minRt - boxSizeX,
            y0: 0,
            x1: maxRt + boxSizeX,
            y1: maxInt + boxSizeY,
            line: {
                color: '#960303',
                width: 2.5,
                dash: 'dash'
            }
        }]
    };
    Plotly.relayout('mainChromatogram', update);
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
        fNetwork: activeSampleData.map(obj => obj.network_features),
        upLowRange: [minRt - minRt * 0.05, maxRt + maxRt * 0.02]
    }
}


function getChromColors(sampleData, peakNumber, isFeatureVisualization) {
    var fillColors = ['rgba(153, 191, 159, 0.70)', 'rgba(252, 224, 151, 0.70)'];
    var lineColors = ['#5a755e', '#fab80f'];
    var legendLabels = ['Selected', 'Blank'];

    var fillColorsFeature = ['rgba(245, 127, 129, 0.70)', 'rgba(66, 135, 245, 0.30)'];
    var lineColorsFeature = ['#960303', '#127aa3'];
    var legendLabelsFeature = ['Selected feature', 'Related feature'];

    if (peakNumber == false && peakNumber!== 0) {
        return isFeatureVisualization ?
        { legLab: legendLabelsFeature, lineCol: lineColorsFeature, fillCol: fillColorsFeature } :
        { legLab: legendLabels, lineCol: lineColors, fillCol: fillColors };
    } else {
        if (isFeatureVisualization == false) {
            switch (sampleData.blankAs[peakNumber]) {
            case true:
                return { lineCol: lineColors[1], fillCol: fillColors[1] };
            case false:
                return { lineCol: lineColors[0], fillCol: fillColors[0] };
            };
        } else {
            switch (sampleData.target[peakNumber]) {
                case 'selected':
                    return { lineCol: lineColorsFeature[0], fillCol: fillColorsFeature[0] };
                case 'related':
                    return { lineCol: lineColorsFeature[1], fillCol: fillColorsFeature[1] };
            }
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