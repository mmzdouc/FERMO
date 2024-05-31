import { getSampleData, getFeatureData } from './parsing.js';
import { updateFeatureTables, hideTables } from './dynamic_tables.js';
import { visualizeData } from './chromatogram.js';
import { visualizeNetwork, hideNetwork } from './network.js';
import { enableDragAndDrop, disableDragAndDrop } from './dragdrop.js';

document.addEventListener('DOMContentLoaded', function() {
    var dragged;
    // Initial state of drag and drop based on checkbox
    var allowDragAndDropCheckbox = document.getElementById('allowDragAndDrop');
    if (allowDragAndDropCheckbox.checked) {
        enableDragAndDrop();
    } else {
        disableDragAndDrop();
    }

    // Toggle drag and drop functionality based on checkbox state
    allowDragAndDropCheckbox.addEventListener('change', function() {
        if (this.checked) {
            enableDragAndDrop();
        } else {
            disableDragAndDrop();
        }
    });


    // Load all data
    var chromatogramElement = document.getElementById('mainChromatogram');
    var networkElement = document.getElementById('cy');
    var statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));
    var statsNetwork = JSON.parse(networkElement.getAttribute('data-stats-network'));

    var firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        var firstSampleName = firstSample.getAttribute('data-sample-name');
        var sampleData = getSampleData(firstSampleName, statsChromatogram);
        visualizeData(sampleData, false);
        document.getElementById('activeSample').textContent = 'Sample: ' + firstSampleName;

        let networkType = 'modified_cosine';
        let sampleId = null;

        // Update the feature table on chromatogram click
        chromatogramElement.on('plotly_click', handleChromatogramClick);
        // Add event listener for network type selection
        document.getElementById('networkSelect').addEventListener('change', handleNetworkTypeChange);
    }

    // Handle chromatogram click event
    function handleChromatogramClick(data) {
        var networkType = document.getElementById('networkSelect').value;
        var featureId = data.points[0].data.name;
        var filteredSampleData = getFeatureData(featureId, sampleData);
        var sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
    }

    // Handle network type selection change event
    function handleNetworkTypeChange() {
        var networkType = document.getElementById('networkSelect').value;
        var featureId = document.getElementById('activeFeature').textContent.split(': ')[1];
        var filteredSampleData = getFeatureData(featureId, sampleData);
        var sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
    }

    // Activate the clicked sample of the 'Sample overview'
    var rows = document.querySelectorAll('.select-sample');
    rows.forEach(function(row) {
        row.addEventListener('click', function() {
            var sampleName = this.getAttribute('data-sample-name');
            sampleData = getSampleData(sampleName, statsChromatogram);
            visualizeData(sampleData, false);
            hideNetwork();
            hideTables();
            document.getElementById('activeSample').textContent = 'Sample: ' + sampleName;
            Plotly.purge('featureChromatogram');
            document.getElementById('feature-general-info').textContent =
            'Click on any feature in the main chromatogram overview.';
            document.getElementById('feature-annotation').textContent =
            'Click on any feature in the main chromatogram overview.';
            Plotly.purge('heatmap-container');
            document.getElementById("sampleCell").innerHTML =
            "<tr><td>Click on any feature in the main chromatogram overview.</td><td></td></tr>";

            let networkType = 'modified_cosine';
            let sampleId = null;

            // Remove previous Plotly click event listeners
            chromatogramElement.removeAllListeners('plotly_click');

            // Attach event listeners again
            chromatogramElement.on('plotly_click', handleChromatogramClick);
            document.getElementById('networkSelect').removeEventListener('change', handleNetworkTypeChange);
            document.getElementById('networkSelect').addEventListener('change', handleNetworkTypeChange);
        });
    });
});
