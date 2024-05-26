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
            for (var i = 0; i < sampleData.featureId.length; i++) {
                if (sampleData.featureId[i] == featureId) {
                    addBoxVisualization(sampleData.traceInt[i], sampleData.traceRt[i]);
                    var filteredSampleData = getFeatureData(featureId, sampleData);
                    visualizeData(filteredSampleData, true);
                    updateTableWithFeatureData(i, sampleData);
                    updateTableWithGroupData(sampleData.fGroupData[i]);
                    updateTableWithSampleData(sampleData.fSampleData[i]);
                    updateTableWithAnnotationData(sampleData.annotations[i]);
                }
            }
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
          document.getElementById("sampleCell").innerHTML =
          "<tr><td>Click on any feature in the main chromatogram overview.</td><td></td></tr>";

          // Update the feature table
          chromatogramElement.on('plotly_click', function(data) {
              var featureId = data.points[0].data.name;
              for (var i = 0; i < sampleData.featureId.length; i++) {
                  if (sampleData.featureId[i] == featureId) {
                      addBoxVisualization(sampleData.traceInt[i], sampleData.traceRt[i]);
                      var filteredSampleData = getFeatureData(featureId, sampleData);
                      visualizeData(filteredSampleData, true);
                      updateTableWithFeatureData(i, sampleData);
                      updateTableWithGroupData(sampleData.fGroupData[i]);
                      updateTableWithSampleData(sampleData.fSampleData[i]);
                      updateTableWithAnnotationData(sampleData.annotations[i], sampleName);
                  }
              }
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
        fSampleData: activeSampleData.map(obj => obj.f_sample),
        annotations: activeSampleData.map(obj => obj.annotations),
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

function addBoxVisualization(traceInt, traceRt) {
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
					showarrow: false,
					font: { size: 7 }
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
			text: `Fold-differences of <br><b>${groupName}</b>`,
			font: { size: 12 },
			x: 0.5,
			xanchor: 'center',
		},
		width: 250,
		height: 250,
		xaxis: {
			ticks: '',
			ticksuffix: ' ',
			autosize: false,
			font: { size: 7 },
		},
		yaxis: {
			ticks: '',
			ticksuffix: ' ',
			autosize: false,
			font: { size: 7 },
		},
		annotations: annotations,
		margin: { l: 50, r: 50, t: 50, b: 50 },
	};

	// Create the heatmap
	Plotly.newPlot('heatmap-container', [trace], layout);
}

// Table update functions //
// TODO: remove general feature data after sample switch
function updateTableWithFeatureData(fId, sampleData) {
    document.getElementById('featureIdCell').textContent = sampleData.featureId[fId];
    document.getElementById('precMzCell').textContent = sampleData.precMz[fId];
    document.getElementById('retTimeCell').textContent = sampleData.retTime[fId];
    document.getElementById('relIntCell').textContent = sampleData.relInt[fId];
    document.getElementById('absIntCell').textContent = sampleData.absInt[fId];
    document.getElementById('NovScore').textContent = sampleData.novScore[fId];
    document.getElementById('BlankAs').textContent = sampleData.blankAs[fId];
}

// TODO: test multiple groups
function updateTableWithGroupData(groupData){
    var featureData = Object.entries(groupData);
    if (Object.keys(featureData).length === 0) {
        document.getElementById('feature-general-info').textContent = 'No group data available for this feature.'
        Plotly.purge('heatmap-container');
    } else {
        document.getElementById('feature-general-info').textContent = 'The feature is found in the following groups:'
        for (const [key, value] of featureData) {
            createHeatmap(value, key);
        }
    }
}

function updateTableWithSampleData(sampleData) {
    let tableBody = document.getElementById("sampleCell");
    tableBody.innerHTML = "";
    let dataArray = sampleData;
    dataArray.forEach(item => {
        let row = document.createElement("tr");
        let sIdCell = document.createElement("td");
        sIdCell.textContent = item.s_id;
        row.appendChild(sIdCell);
        let valueCell = document.createElement("td");
        valueCell.textContent = item.value;
        row.appendChild(valueCell);
        tableBody.appendChild(row);
    });
}
// TODO: remove feature data after sample switch
function updateTableWithAnnotationData(annotations, sample) {
    // Define headers and columns for each section
    let matchHeaders = ["Match id", "Score", "More info"];
    let matchColumns = ["id", "score"];
    let matchExtraColumns = [
        { title: "Algorithm", field: "algorithm" },
        { title: "Mz", field: "mz" },
        { title: "Difference in mz", field: "diff_mz" },
        { title: "SMILES", field: "smiles" },
        { title: "Link to MIBiG", field: "id" }
    ];

    let lossHeaders = ["Loss id", "Difference in ppm", "More info"];
    let lossColumns = ["id", "diff_ppm"];
    let lossExtraColumns = [
        { title: "Detected loss", field: "det_loss" },
        { title: "Expected loss", field: "exp_loss" },
        { title: "Fragment mz", field: "mz_frag" }
    ];

    let fragmentHeaders = ["Fragment id", "Difference in ppm", "More info"];
    let fragmentColumns = ["id", "diff_ppm"];
    let fragmentExtraColumns = [
        { title: "Detected fragment", field: "frag_det" },
        { title: "Expected fragment", field: "frag_ex" }
    ];

    let adductHeaders = ["Adduct type", "Difference in ppm", "More info"];
    let adductColumns = ["adduct_type", "diff_ppm"];
    let adductExtraColumns = [
        { title: "Partner adduct", field: "partner_adduct" },
        { title: "Partner mz", field: "partner_mz" },
        { title: "Partner id", field: "partner_id" },
        { title: "difference in ppm", field: "diff_ppm" }
    ];

    // create tables for each section
    let isAnyDataPresent = false;

    isAnyDataPresent = createAnnotationTable("matchTable", annotations.matches, matchHeaders,
    matchColumns, matchExtraColumns, "match") || isAnyDataPresent;
    isAnyDataPresent = createAnnotationTable("lossesTable", annotations.losses, lossHeaders,
    lossColumns, lossExtraColumns, "loss") || isAnyDataPresent;
    isAnyDataPresent = createAnnotationTable("fragmentTable", annotations.fragments, fragmentHeaders,
    fragmentColumns, fragmentExtraColumns, "fragment") || isAnyDataPresent;
    isAnyDataPresent = createAnnotationTable("adductTable", annotations.adducts, adductHeaders,
    adductColumns, adductExtraColumns, "adduct") || isAnyDataPresent;

    let annMessage = document.getElementById("feature-annotation");
    if (!isAnyDataPresent) {
        annMessage.innerHTML = "No annotation data found for this feature.";
    }
}

function createAnnotationTable(sectionId, annotations, headers, columns, extraColumns, tableId) {
    let tableBody = document.getElementById(sectionId);
    tableBody.innerHTML = "";

    let annMessage = document.getElementById("feature-annotation");
    annMessage.innerHTML = "";

    if (annotations.length > 0) {
        let tHead = createTableHeader(headers);
        tableBody.appendChild(tHead);

        let tBody = createTableBody(annotations, columns, extraColumns, tableId);
        tableBody.appendChild(tBody);

        tableBody.style.marginBottom = "1rem";
        return true;
    } else {
        tableBody.style.marginBottom = "0";
        return false;
    }
}

function createTableHeader(headers) {
    let tHead = document.createElement("thead");
    let rowHead = document.createElement("tr");

    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        rowHead.appendChild(th);
    });

    tHead.appendChild(rowHead);
    return tHead;
}

function createTableRow(data, columns, rowId, tableId) {
    let row = document.createElement("tr");

    columns.forEach(column => {
        let td = document.createElement("td");
        let cellData = data[column];
        if (typeof cellData === 'string' && cellData.includes("|")) {
            td.textContent = cellData.split("|")[0];
        } else {
            td.textContent = cellData !== undefined ? cellData : '';
        }
        row.appendChild(td);
    });

    // Add the collapse button for expanding extra info
    let expandCell = document.createElement("td");
    expandCell.className = "text-center";
    let expandButton = document.createElement("button");
    expandButton.className = "accordion-button-info collapsed";
    expandButton.type = "button";
    expandButton.setAttribute("data-bs-toggle", "collapse");
    expandButton.setAttribute("data-bs-target", `#collapse-${tableId}-${rowId}`);
    expandButton.setAttribute("aria-expanded", "false");
    expandButton.setAttribute("aria-controls", `collapse-${tableId}-${rowId}`);

    expandCell.appendChild(expandButton);
    row.appendChild(expandCell);

    return row;
}

function createTableBody(dataArray, columns, extraColumns, tableId) {
    let tBody = document.createElement("tbody");

    dataArray.forEach((data, index) => {
        let row = createTableRow(data, columns, index, tableId);
        tBody.appendChild(row);

        // Create the extra info row
        let extraInfoRow = document.createElement("tr");
        let extraInfoCell = document.createElement("td");
        extraInfoCell.colSpan = columns.length + 4;
        extraInfoCell.style.padding = "0px";

        let collapseDiv = document.createElement("div");
        collapseDiv.id = `collapse-${tableId}-${index}`;
        collapseDiv.className = "collapse";

        let { extraInfo } = createExtraInfoRow(data, extraColumns, columns.length + 1);
        collapseDiv.appendChild(extraInfo);

        extraInfoCell.appendChild(collapseDiv);
        extraInfoRow.appendChild(extraInfoCell);

        tBody.appendChild(extraInfoRow);
    });

    return tBody;
}

function clickToCopy(data, displayText) {
    const span = document.createElement("span");
    span.textContent = displayText;
    span.style.cursor = "pointer";
    span.style.color = "rgba(13, 110, 253)";

    span.onclick = function() {
        const tempInput = document.createElement("input");
        tempInput.value = data;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);

        alert("Copied to clipboard: \n" + data);
    };

    return span;
}

function createExtraInfoRow(data, extraColumns, colspan) {
    let extraInfo = document.createElement("div");
    extraInfo.style.padding = "10px";
    extraInfo.style.backgroundColor = "#f9f9f9";
    extraInfo.style.fontSize = "0.8em";

    let infoTable = document.createElement("table");
    infoTable.classList.add("fixed-width-table-extra");

    extraColumns.forEach(column => {
        let cellData = data[column.field];
        let infoRow = document.createElement("tr");

        let titleCell = document.createElement("td");
        titleCell.textContent = column.title + ":";
        titleCell.style.fontWeight = "bold";
        infoRow.appendChild(titleCell);

        let valueCell = document.createElement("td");
        if (column.title === "Link to MIBiG") {
            if (typeof cellData === 'string' && cellData.includes("|")) {
                let mibigLink = document.createElement('a');
                mibigLink.href = `https://mibig.secondarymetabolites.org/repository/${cellData.split("|")[1]}`;
                mibigLink.textContent = cellData.split("|")[1];
                mibigLink.target = "_blank";
                valueCell.appendChild(mibigLink);
            } else {
                return;
            }
        } else {
            valueCell.textContent = cellData !== undefined ? cellData : '';
        }

        if (column.title === "SMILES") {
            let displayText = "Copy SMILES";
            let copySpan = clickToCopy(cellData, displayText);
            valueCell.innerHTML = '';
            valueCell.appendChild(copySpan);
        }

        infoRow.appendChild(valueCell);
        infoTable.appendChild(infoRow);
    });

    extraInfo.appendChild(infoTable);

    return { extraInfo };
}