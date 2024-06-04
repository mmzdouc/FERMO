import { getSampleData, getFeatureData } from './parsing.js';
import { updateFeatureTables, hideTables } from './dynamic_tables.js';
import { visualizeData, addBoxVisualization } from './chromatogram.js';
import { visualizeNetwork, hideNetwork } from './network.js';
import { enableDragAndDrop, disableDragAndDrop } from './dragdrop.js';
import { updateRangeFromSlider, updateRangeFromInput,
         enforceConstraints, initializeFilters, getFeaturesWithinRange } from './filters.js';

document.addEventListener('DOMContentLoaded', function() {
    var dragged;
    var currentBoxParams = null;
    var sampleData;
    var statsChromatogram;
    var statsNetwork;

    function getCurrentBoxParams() {
        return currentBoxParams;
    }

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
    statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));
    statsNetwork = JSON.parse(networkElement.getAttribute('data-stats-network'));

    var firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        var firstSampleName = firstSample.getAttribute('data-sample-name');
        sampleData = getSampleData(firstSampleName, statsChromatogram);
        visualizeData(sampleData, false, 0, 1);
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
        currentBoxParams = { traceInt: sampleData.traceInt[sampleId], traceRt: sampleData.traceRt[sampleId] };
        addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
    }

    // Handle network type selection change event
    function handleNetworkTypeChange() {
        var networkType = document.getElementById('networkSelect').value;
        var featureId = document.getElementById('activeFeature').textContent.split(': ')[1];
        var filteredSampleData = getFeatureData(featureId, sampleData);
        var sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
        currentBoxParams = { traceInt: sampleData.traceInt[sampleId], traceRt: sampleData.traceRt[sampleId] };
    }

    var annotationFeatureCheckbox = document.getElementById('showAnnotationFeatures');

    annotationFeatureCheckbox.addEventListener('change', function() {
        var isChecked = this.checked;
        var annotationRelatedContainers = document.querySelectorAll('.annotation-related');

        annotationRelatedContainers.forEach(function(container) {
            if (isChecked) {
                container.style.display = 'block';
            } else {
                container.style.display = 'none';
            }
        });
    });

    document.getElementById('groupButton').addEventListener('click', function() {
        var dropdownContainer = document.getElementById('dropdownGroupContainer');
        if (dropdownContainer.style.display === "none" || dropdownContainer.style.display === "") {
            dropdownContainer.style.display = "block";
        } else {
            dropdownContainer.style.display = "none";
        }
    });
    document.getElementById('networkExcludeButton').addEventListener('click', function() {
        var dropdownContainer = document.getElementById('dropdownNetworkContainer');
        if (dropdownContainer.style.display === "none" || dropdownContainer.style.display === "") {
            dropdownContainer.style.display = "block";
        } else {
            dropdownContainer.style.display = "none";
        }
    });

    // Activate the clicked sample of the 'Sample overview'
    var rows = document.querySelectorAll('.select-sample');
    rows.forEach(function(row) {
        row.addEventListener('click', function() {
            var sampleName = this.getAttribute('data-sample-name');
            sampleData = getSampleData(sampleName, statsChromatogram);
            visualizeData(sampleData, false, parseFloat(document.getElementById('noveltyRange1').value), parseFloat(document.getElementById('noveltyRange2').value));
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
            currentBoxParams = null;

            // Remove previous Plotly click event listeners
            chromatogramElement.removeAllListeners('plotly_click');

            // Attach event listeners again
            chromatogramElement.on('plotly_click', handleChromatogramClick);
            document.getElementById('networkSelect').removeEventListener('change', handleNetworkTypeChange);
            document.getElementById('networkSelect').addEventListener('change', handleNetworkTypeChange);

            initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures,
                  sampleData, chromatogramElement, getCurrentBoxParams);
            // Call updateRange immediately after initializing filters
            const noveltyRange1 = document.getElementById('noveltyRange1');
            const noveltyRange2 = document.getElementById('noveltyRange2');
            const phenotypeRange1 = document.getElementById('phenotypeRange1');
            const phenotypeRange2 = document.getElementById('phenotypeRange2');
            const showPhenotypeFeatures = document.getElementById('showPhenotypeFeatures');

            function updateRange() {
                var minScore = parseFloat(noveltyRange1.value);
                var maxScore = parseFloat(noveltyRange2.value);
                var minPhenotypeScore = parseFloat(phenotypeRange1.value);
                var maxPhenotypeScore = parseFloat(phenotypeRange2.value);
                var showOnlyPhenotypeFeatures = showPhenotypeFeatures.checked;

                visualizeData(sampleData, false, minScore, maxScore, minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures);
                chromatogramElement.on('plotly_click', handleChromatogramClick);
                // Reapply the box visualization if it was previously set
                if (currentBoxParams) {
                    addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
                }
                updateRetainedFeatures(minScore, maxScore, minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures);
            }
            updateRange();
        });
    });

    function updateRetainedFeatures(minScore, maxScore, minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures) {
        rows.forEach(function(row) {
            var sampleName = row.getAttribute('data-sample-name');
            var sampleData = getSampleData(sampleName, statsChromatogram);
            var featuresWithinRange = getFeaturesWithinRange(sampleData, minScore, maxScore, minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures);
            row.children[2].textContent = featuresWithinRange;
        });
    }

    // Initialize filters
    initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures,
                      sampleData, chromatogramElement, getCurrentBoxParams);
});