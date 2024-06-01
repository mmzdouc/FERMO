// Chromatogram visualization functions //
export function visualizeData(sampleData, isFeatureVisualization = false, minScore = 0, maxScore = 10) {
    var data = [];
    var maxPeaksPerSample = sampleData.traceInt.map(trace => Math.max(...trace));
    var featuresWithinRange = 0;

    var combinedData = sampleData.traceRt.map((rt, i) => ({
        traceRt: rt,
        traceInt: sampleData.traceInt[i],
        featureId: sampleData.featureId[i],
        maxPeak: maxPeaksPerSample[i],
        chromColors: getChromColors(sampleData, i, isFeatureVisualization),
        toolTip: getToolTip(sampleData, i),
        novScore: sampleData.novScore[i]
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

        if ( isFeatureVisualization === false ) {
            if (dataItem.novScore >= minScore && dataItem.novScore <= maxScore) {
                featuresWithinRange++;
            } else {
                result.line.color = 'rgba(212, 212, 212, 0.8)';
                result.fillcolor = 'rgba(212, 212, 212, 0.3)';
            }
        }

        data.push(result);
    });

    console.log(`Features within the range ${minScore}-${maxScore}: ${featuresWithinRange}`);
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
        height: isFeatureVisualization ? 125 : 227,
        margin: {
            l: 50, r: 0, t: 0,
            b: isFeatureVisualization ? 35 : 30,
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

export function addBoxVisualization(traceInt, traceRt) {
    var boxSizeX = 0.12;
    var boxSizeY = 0.04;
    var maxInt = Math.max(...traceInt);
    var maxRt = Math.max(...traceRt);
    var minRt = Math.min(...traceRt);

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