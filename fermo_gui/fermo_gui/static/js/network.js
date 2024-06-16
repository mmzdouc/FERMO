/* Script to create the CytoScape network elements

Copyright (c) 2024-present Hannah Esther Augustijn, MSc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

import { getUniqueFeatureIds, getFeatureDetails, getFeatureData } from './parsing.js';
import { updateFeatureTables } from './dynamic_tables.js';

export function visualizeNetwork(fId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType) {
    const cos_id = sampleData.idNetCos[sampleId];
    const ms_id = sampleData.idNetMs[sampleId];
    const networkId = networkType === 'modified_cosine' ? cos_id : ms_id;

    const filteredFeatureIds = filteredSampleData.featureId.filter(id => id.toString() !== fId);
    const networkData = statsNetwork[networkType][networkId].elements;
    const uniqueNIds = networkData.nodes.map(node => node.data.id);
    const uniqueFIds = getUniqueFeatureIds(statsChromatogram);
    const featureDetails = getFeatureDetails(uniqueNIds, statsChromatogram);

    const cy = cytoscape({
        container: document.getElementById('cy'),
        elements: networkData,
        layout: { name: 'cose', rows: 1 },
        style: getCyStyles(fId, filteredFeatureIds, uniqueFIds)
    });

    const tooltip = createTooltip();
    setupCyEvents(cy, tooltip, featureDetails, sampleData, fId, statsNetwork, statsChromatogram, networkType);
    showNetwork();
}

function getCyStyles(fId, filteredFeatureIds, uniqueFIds) {
    return [
        { selector: 'node', style: baseNodeStyle("#b2b6b9", "white") },
        { selector: 'edge', style: { "curve-style": "bezier", "width": "mapData(weight, 0.5, 1, 1, 10)" } },
        { selector: `node[id = "${fId}"]`, style: baseNodeStyle("#f4aaa7", "#960303") },
        { selector: filteredFeatureIds.map(id => `node[id = "${id}"]`).join(', '), style: baseNodeStyle("#c6dcfb", "#227aa0") },
        { selector: uniqueFIds.map(id => `node[id = "${id}"]`).join(', '), style: { "border-color": "#000", "border-width": 4 } },
        { selector: 'edge:selected', style: { 'line-color': '#F08080', "target-arrow-color": "#F08080" } }
    ];
}

function baseNodeStyle(bgColor, borderColor) {
    return { "background-color": bgColor, "border-color": borderColor, "border-width": 4, color: "white" };
}

function createTooltip() {
    const tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    document.body.appendChild(tooltip);
    return tooltip;
}

function setupCyEvents(cy, tooltip, featureDetails, sampleData, fId, statsNetwork, statsChromatogram, networkType) {
    cy.on('mouseover', 'node', event => showNodeTooltip(event.target, featureDetails, tooltip));
    cy.on('mousemove', 'node', event => moveTooltip(event, tooltip));
    cy.on('mouseout', 'node', () => hideTooltip(tooltip));
    cy.on('mouseover', 'edge', event => showEdgeTooltip(event.target, featureDetails, tooltip));
    cy.on('mousemove', 'edge', event => moveTooltip(event, tooltip));
    cy.on('mouseout', 'edge', () => hideTooltip(tooltip));

    cy.on('select', 'node', event => handleNodeSelect(event.target, featureDetails, sampleData, fId, statsNetwork, statsChromatogram, networkType, tooltip));
    document.getElementById('cy').addEventListener('mouseleave', () => hideTooltip(tooltip));
}

function showNodeTooltip(node, featureDetails, tooltip) {
    const featureId = node.id();
    const featureDetail = featureDetails.find(feature => feature.f_id.toString() === featureId);

    if (featureDetail) {
        tooltip.innerHTML = `Feature ID: ${featureId}<br>
                             Precursor m/z: ${featureDetail.mz}<br>
                             Average rt: ${featureDetail.rt_avg}<br>`;
        tooltip.style.display = 'block';
    }
}

function showEdgeTooltip(edge, featureDetails, tooltip) {
    const edgeWeight = edge.data('weight').toFixed(2);
    const sourceId = edge.data('source').toString();
    const targetId = edge.data('target').toString();
    const sourceFeature = featureDetails.find(feature => feature.f_id.toString() === sourceId);
    const targetFeature = featureDetails.find(feature => feature.f_id.toString() === targetId);

    if (sourceFeature && targetFeature) {
        const mzDifference = Math.abs(sourceFeature.mz - targetFeature.mz).toFixed(4);
        tooltip.innerHTML = `Edge Weight: ${edgeWeight}<br>m/z Difference: ${mzDifference}<br>`;
        tooltip.style.display = 'block';
    }
}

function moveTooltip(event, tooltip) {
    tooltip.style.left = event.originalEvent.pageX + 10 + 'px';
    tooltip.style.top = event.originalEvent.pageY + 10 + 'px';
}

function hideTooltip(tooltip) {
    tooltip.style.display = 'none';
}

function handleNodeSelect(node, featureDetails, sampleData, fId, statsNetwork, statsChromatogram, networkType, tooltip) {
    hideTooltip(tooltip);
    const featureId = node.id();
    const filteredSampleData = getFeatureData(featureId, sampleData, networkType);

    if (isEmpty(filteredSampleData)) {
        alert('This feature is not found in this sample.');
    } else {
        const sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
    }
}

function isEmpty(data) {
    return Object.values(data).every(array => Array.isArray(array) && array.length === 0);
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