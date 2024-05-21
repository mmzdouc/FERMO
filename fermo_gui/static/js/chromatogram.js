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
            updateTableWithGroupData(featureId, sampleData);
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
          document.getElementById('feature-general-info').textContent = 'Click on any feature in the main chromatogram overview.'
          Plotly.purge('heatmap-container');

          // Update the feature table
          chromatogramElement.on('plotly_click', function(data) {
              var featureId = data.points[0].data.name;
              updateTableWithFeatureData(featureId, sampleData);
              addBoxVisualization(featureId, sampleData);
              var filteredSampleData = getFeatureData(featureId, sampleData);
              visualizeData(filteredSampleData, true);
              updateTableWithGroupData(featureId, sampleData);
          });
       });
    });
});

// Data extraction functions //
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
        samples: activeSampleData.map(obj => obj.samples),
        fGroupData: activeSampleData.map(obj => obj.f_group),
        upLowRange: [minRt - minRt * 0.05, maxRt + maxRt * 0.02]
    }
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
                    filteredData.target.push(sampleData.featureId[index] == featureId ? 'selected' : 'related');
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

// Chromatogram visualization functions //
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
        data.push(createLegendItem(legLab[i], fillCol[i], lineCol[i], 'square'));
    }
    if (!isFeatureVisualization) {
        data.push(createLegendItem('Unique to sample', '#000000'));
        data.push(createLegendItem('Selected feature', '#960303'));
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

function createLegendItem(name, color, lineCol, type = 'line') {
    const legendItem = {
        x: [null],
        y: [null],
        mode: 'markers',
        name: name,
        showlegend: true
    };

    if (type === 'line') {
        legendItem.marker = {
            size: 8,
            symbol: 'line-ew',
            line: {
                color: color,
                width: 2
            }
        };
    } else if (type === 'square') {
        legendItem.marker = {
            size: 10,
            symbol: 'square',
            color: color,
            line: {
                color: lineCol,
                width: 2
            }
        };

    }
    return legendItem;
}

function getChromColors(sampleData, peakNumber, isFeatureVisualization) {
    const colors = {
        default: {
            fillColors: ['rgba(153, 191, 159, 0.70)', 'rgba(252, 224, 151, 0.70)'],
            lineColors: ['#5a755e', '#fab80f'],
            legendLabels: ['Selected', 'Blank']
        },
        feature: {
            fillColors: ['rgba(245, 127, 129, 0.70)', 'rgba(66, 135, 245, 0.30)'],
            lineColors: ['#960303', '#127aa3'],
            legendLabels: ['Selected feature', 'Related feature']
        }
    };

    const colorSet = isFeatureVisualization ? colors.feature : colors.default;

    if (peakNumber === false || peakNumber === undefined) {
        return {
            legLab: colorSet.legendLabels,
            lineCol: colorSet.lineColors,
            fillCol: colorSet.fillColors
        };
    }

    if (!isFeatureVisualization) {
        const isBlank = sampleData.blankAs[peakNumber];
        const isSingleSample = sampleData.samples[peakNumber].length === 1;
        const index = isBlank ? 1 : 0;
        return {
            lineCol: isSingleSample ? '#000000' : colorSet.lineColors[index],
            fillCol: colorSet.fillColors[index]
        };
    } else {
        const targetType = sampleData.target[peakNumber];
        if (targetType === 'selected') {
            return { lineCol: colorSet.lineColors[0], fillCol: colorSet.fillColors[0] };
        } else if (targetType === 'related') {
            return { lineCol: colorSet.lineColors[1], fillCol: colorSet.fillColors[1] };
        }
    }
}

function getToolTip(sampleData, peakNumber) {
    return `&nbsp;Feature ID: ${sampleData.featureId[peakNumber]}<br>
            Precursor m/z: ${sampleData.precMz[peakNumber]}<br>
            Retention time: ${sampleData.retTime[peakNumber]}<br>
            Relative intensity: ${sampleData.relInt[peakNumber]}<br>
            Absolute intensity: ${sampleData.absInt[peakNumber]}<br>`
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

// Heatmap visualization functions //
function createHeatmap(data, groupName) {
	const groupValues = [...new Set([...data.map(item => item.group1), ...data.map(item => item.group2)])].sort();
	const matrix = groupValues.map(() => Array(groupValues.length).fill(0));

	// Fill the matrix with factor values
	data.forEach(item => {
		const rowIndex = groupValues.indexOf(item.group1);
		const colIndex = groupValues.indexOf(item.group2);
		matrix[rowIndex][colIndex] = item.factor;
		matrix[colIndex][rowIndex] = item.factor;
	});
	const reversedMatrix = matrix.reverse();
	const reversedGroupValues = [...groupValues].reverse();

	// Create value annotations to be shown within the heatmap
	const annotations = [];
	for (let i = 0; i < reversedGroupValues.length; i++) {
		for (let j = 0; j < groupValues.length; j++) {
			if (reversedMatrix[i][j] !== null) {
				annotations.push({
					x: groupValues[j],
					y: reversedGroupValues[i],
					text: reversedMatrix[i][j].toFixed(2),
					showarrow: false
				});
			}
		}
	}

	// Define colorscale
	const colorscaleValue = [
		[0, '#f5f5f5'],
		[0.01, '#dbf3ff'],
		[1, '#de4b4b']
	];

	// Create a new Plotly figure
	const trace = {
		z: reversedMatrix,
		x: groupValues,
		y: reversedGroupValues,
		type: 'heatmap',
		colorscale: colorscaleValue,
		showscale: false
	};

	// Define layout options
	const layout = {
		title: {
			text: `<b>${groupName}</b>`,
			font: { size: 12 },
			x: 0.5,
			xanchor: 'center',
		},
		width: 350,
		height: 350,
		xaxis: {
			ticks: '',
			ticksuffix: ' ',
			autosize: false,
		},
		yaxis: {
			ticks: '',
			ticksuffix: ' ',
			autosize: false,
		},
		annotations: annotations,
		margin: { l: 50, r: 50, t: 50, b: 50 },
	};

	// Create the heatmap
	Plotly.newPlot('heatmap-container', [trace], layout);
}

// Table update functions //
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

// TODO: test multiple groups
function updateTableWithGroupData(featureId, sampleData){
    for (var i = 0; i < sampleData.featureId.length; i++) {
        if (sampleData.featureId[i] == featureId) {
            var featureData = Object.entries(sampleData.fGroupData[i]);
            if (Object.keys(featureData).length === 0) {
                document.getElementById('feature-general-info').textContent = 'No group data available for this feature.'
                Plotly.purge('heatmap-container');
            } else {
                document.getElementById('feature-general-info').textContent = 'Fold-differences across:'
                for (const [key, value] of featureData) {
                    createHeatmap(value, key);
                }
            }
        }
    }
}
