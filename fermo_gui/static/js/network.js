import { getUniqueFeatureIds, getFeatureDetails } from './parsing.js';
import { updateFeatureTables } from './dynamic_tables.js';

export function visualizeNetwork(fId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram) {
    var filteredFeatureIds = filteredSampleData.featureId.filter(id => id.toString() !== fId);
    var cos_id = sampleData.idNetCos[sampleId]
    var ms_id = sampleData.idNetMs[sampleId]

    // Get all feature info for tool tips and table information
    const uniqueNIds = [];
    var networkNodes = statsNetwork.modified_cosine[cos_id].elements.nodes;
    for (var i = 0; i < networkNodes.length; i++) {
        uniqueNIds.push(networkNodes[i].data.id);
    }
    const uniqueFIds = getUniqueFeatureIds(statsChromatogram);
    const featureDetails = getFeatureDetails(uniqueNIds, statsChromatogram);

    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: statsNetwork.modified_cosine[cos_id].elements,

        layout: {
            name: 'cose',
            rows: 1
        },

        style: [
            {
                selector: 'node',
                style: {
                    "background-color": "#b2b6b9",
                    color: "white",
                    "border-color": "white",
                    "border-width": 4
                }
            },
            {
                selector: 'edge',
                style: {
                    "curve-style": "bezier",
                    "width": "mapData(weight, 0.5, 1, 1, 10)"
                }
            },
            {
                selector: 'node[id = "' + fId + '"]',
                style: {
                    "background-color": "#f4aaa7",
                    "border-color": "#960303",
                    "border-width": 4
                }
            },
            {
                selector: filteredFeatureIds.map(id => 'node[id = "' + id + '"]').join(', '),
                style: {
                    "background-color": "#c6dcfb",
                    "border-color": "#227aa0",
                    "border-width": 4
                }
            },
            {
                selector: uniqueFIds.map(id => 'node[id = "' + id + '"]').join(', '),
                style: {
                    "border-color": "#000",
                    "border-width": 4
                }
            },
            {
                selector: 'edge:selected',
                style: {
                    'line-color': '#F08080',
                    "target-arrow-color": "#F08080",
                }
            },
        ],

    });

    var tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    document.body.appendChild(tooltip);

    // Show tooltip on mouseover
    cy.on('mouseover', 'node', function (event) {
        var node = event.target;
        var featureId = node.id();
        var featureDetail = featureDetails.find(feature => feature.f_id.toString() === featureId);

        tooltip.innerHTML =
        'Feature ID: ' + node.id() + '<br>' +
        'Precursor m/z: ' + featureDetail.mz + '<br>' +
        'Average rt: ' + featureDetail.rt_avg + '<br>';
        tooltip.style.display = 'block';
    });

    cy.on('mousemove', 'node', function (event) {
        tooltip.style.left = event.originalEvent.pageX + 10 + 'px';
        tooltip.style.top = event.originalEvent.pageY + 10 + 'px';
    });

    cy.on('mouseout', 'node', function () {
        tooltip.style.display = 'none';
    });
    document.getElementById('cy').addEventListener('mouseleave', function () {
        tooltip.style.display = 'none';
    });


    cy.on('mouseover', 'edge', function (event) {
        var edge = event.target;
        var edgeWeight = edge.data('weight').toFixed(2);

        var sourceId = edge.data('source').toString();
        var targetId = edge.data('target').toString();

        var sourceFeature = featureDetails.find(feature => feature.f_id.toString() === sourceId);
        var targetFeature = featureDetails.find(feature => feature.f_id.toString() === targetId);

        if (sourceFeature && targetFeature) {
            var mzDifference = Math.abs(sourceFeature.mz - targetFeature.mz).toFixed(4);

            tooltip.innerHTML =
            'Edge Weight: ' + edgeWeight + '<br>' +
            'm/z Difference: ' + mzDifference + '<br>';
            tooltip.style.display = 'block';
        }
    });

    cy.on('mousemove', 'edge', function (event) {
        tooltip.style.left = event.originalEvent.pageX + 10 + 'px';
        tooltip.style.top = event.originalEvent.pageY + 10 + 'px';
    });

    cy.on('mouseout', 'edge', function () {
        tooltip.style.display = 'none';
    });

    cy.on('select', 'node', function(event) {
        tooltip.style.display = 'none';
        var node = event.target;
        var featureId = node.id();
        updateFeatureTables(featureId, sampleData, statsNetwork);
    });
    showNetwork();
}

function showNetwork() {
    document.getElementById('cy-container').style.display = '';
    document.getElementById('legend').style.display = '';
}

export function hideNetwork() {
    document.getElementById('cy-container').style.display = 'none';
    document.getElementById('activeFeature').innerHTML =
    'Select any feature in the main chromatogram to visualize its network.';
    document.getElementById('legend').style.display = 'none';
}
