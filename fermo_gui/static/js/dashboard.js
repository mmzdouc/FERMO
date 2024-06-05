import { getSampleData, getFeatureData } from './parsing.js';
import { updateFeatureTables, hideTables } from './dynamic_tables.js';
import { visualizeData, addBoxVisualization } from './chromatogram.js';
import { visualizeNetwork, hideNetwork } from './network.js';
import { enableDragAndDrop, disableDragAndDrop } from './dragdrop.js';
import { initializeFilters, getFeaturesWithinRange, getFilterGroupSelectionFields } from './filters.js';

document.addEventListener('DOMContentLoaded', function() {
    let dragged;
    let currentBoxParams = null;
    let sampleData;
    let statsChromatogram;
    let statsNetwork;
    let statsGroups;

    const getCurrentBoxParams = () => currentBoxParams;

    const allowDragAndDropCheckbox = document.getElementById('allowDragAndDrop');
    allowDragAndDropCheckbox.checked ? enableDragAndDrop() : disableDragAndDrop();

    allowDragAndDropCheckbox.addEventListener('change', function() {
        this.checked ? enableDragAndDrop() : disableDragAndDrop();
    });

    const chromatogramElement = document.getElementById('mainChromatogram');
    const networkElement = document.getElementById('cy');
    const groupElement = document.getElementById('groupInfo');
    statsChromatogram = JSON.parse(chromatogramElement.getAttribute('data-stats-chromatogram'));
    statsNetwork = JSON.parse(networkElement.getAttribute('data-stats-network'));
    statsGroups = JSON.parse(groupElement.getAttribute('data-stats-groups'));

    const firstSample = document.querySelector('.select-sample');
    if (firstSample) {
        const firstSampleName = firstSample.getAttribute('data-sample-name');
        sampleData = getSampleData(firstSampleName, statsChromatogram);
        document.getElementById('activeSample').textContent = `Sample: ${firstSampleName}`;

        const networkType = 'modified_cosine';

        getFilterGroupSelectionFields(statsGroups)

        Plotly.newPlot(chromatogramElement, []);
        chromatogramElement.on('plotly_click', handleChromatogramClick);
        document.getElementById('networkSelect').addEventListener('change', handleNetworkTypeChange);
        document.getElementById('showBlankFeatures').addEventListener('change', updateRange);
        document.getElementById('findInput').addEventListener('input', updateRange);
        document.getElementById('mz2Input').addEventListener('input', updateRange);
        document.getElementById('sample2Input').addEventListener('input', updateRange);
        document.getElementById('foldInput').addEventListener('input', updateRange);
        document.getElementById('group1FoldInput').addEventListener('input', updateRange);
        document.getElementById('group2FoldInput').addEventListener('input', updateRange);
        document.getElementById('selectFoldInput').addEventListener('change', updateRange);
        document.getElementById('showAnnotationFeatures').addEventListener('change', function() {
            const isChecked = this.checked;
            updateRange();
            document.querySelectorAll('.annotation-related').forEach(container => {
                container.style.display = isChecked ? 'block' : 'none';
            });
        });

        updateRange();
    }

    function handleChromatogramClick(data) {
        const networkType = document.getElementById('networkSelect').value;
        const featureId = data.points[0].data.name;
        const filteredSampleData = getFeatureData(featureId, sampleData);
        const sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
        currentBoxParams = { traceInt: sampleData.traceInt[sampleId], traceRt: sampleData.traceRt[sampleId] };
        addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
    }

    function handleNetworkTypeChange() {
        const networkType = document.getElementById('networkSelect').value;
        const featureId = document.getElementById('activeFeature').textContent.split(': ')[1];
        const filteredSampleData = getFeatureData(featureId, sampleData);
        const sampleId = updateFeatureTables(featureId, sampleData, filteredSampleData);
        visualizeNetwork(featureId, statsNetwork, filteredSampleData, sampleData, sampleId, statsChromatogram, networkType);
        currentBoxParams = { traceInt: sampleData.traceInt[sampleId], traceRt: sampleData.traceRt[sampleId] };
    }

    function toggleDropdown(containerId) {
        const dropdownContainer = document.getElementById(containerId);
        dropdownContainer.style.display = (dropdownContainer.style.display === "none" || dropdownContainer.style.display === "") ? "block" : "none";
    }

    document.getElementById('groupButton').addEventListener('click', () => toggleDropdown('dropdownGroupContainer'));
    document.getElementById('networkExcludeButton').addEventListener('click', () => toggleDropdown('dropdownNetworkContainer'));

    document.querySelectorAll('.select-sample').forEach(row => {
        row.addEventListener('click', function() {
            const sampleName = this.getAttribute('data-sample-name');
            sampleData = getSampleData(sampleName, statsChromatogram);
            hideNetwork();
            hideTables();
            document.getElementById('activeSample').textContent = `Sample: ${sampleName}`;
            Plotly.purge('featureChromatogram');
            document.getElementById('feature-general-info').textContent =
            'Click on any feature in the main chromatogram overview.';
            document.getElementById('feature-annotation').textContent =
            'Click on any feature in the main chromatogram overview.';
            Plotly.purge('heatmap-container');
            document.getElementById("sampleCell").innerHTML =
            "<tr><td>Click on any feature in the main chromatogram overview.</td><td></td></tr>";

            const networkType = 'modified_cosine';
            currentBoxParams = null;

            chromatogramElement.removeAllListeners('plotly_click');
            chromatogramElement.on('plotly_click', handleChromatogramClick);
            document.getElementById('networkSelect').removeEventListener('change', handleNetworkTypeChange);
            document.getElementById('networkSelect').addEventListener('change', handleNetworkTypeChange);
            document.getElementById('showAnnotationFeatures').addEventListener('change', updateRange);
            document.getElementById('showBlankFeatures').addEventListener('change', updateRange);
            document.getElementById('showBlankFeatures').addEventListener('input', updateRange);
            document.getElementById('mz2Input').addEventListener('input', updateRange);
            document.getElementById('sample2Input').addEventListener('input', updateRange);
            document.getElementById('foldInput').addEventListener('input', updateRange);
            document.getElementById('group1FoldInput').addEventListener('input', updateRange);
            document.getElementById('group2FoldInput').addEventListener('input', updateRange);
            document.getElementById('selectFoldInput').addEventListener('change', updateRange);

            initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures,
                sampleData, chromatogramElement, getCurrentBoxParams);

            updateRange();
        });
    });

    function updateRange() {
        const minScore = parseFloat(document.getElementById('noveltyRange1').value);
        const maxScore = parseFloat(document.getElementById('noveltyRange2').value);
        const minPhenotypeScore = parseFloat(document.getElementById('phenotypeRange1').value);
        const maxPhenotypeScore = parseFloat(document.getElementById('phenotypeRange2').value);
        const showOnlyPhenotypeFeatures = document.getElementById('showPhenotypeFeatures').checked;
        const minMatchScore = parseFloat(document.getElementById('matchRange1').value);
        const maxMatchScore = parseFloat(document.getElementById('matchRange2').value);
        const showOnlyMatchFeatures = document.getElementById('showMatchFeatures').checked;
        const showOnlyAnnotationFeatures = document.getElementById('showAnnotationFeatures').checked;
        const showOnlyBlankFeatures = document.getElementById('showBlankFeatures').checked;
        const findFeatureId = parseFloat(document.getElementById('findInput').value);
        const minMzScore = parseFloat(document.getElementById('mz1Input').value);
        const maxMzScore = parseFloat(document.getElementById('mz2Input').value);
        const minSampleCount = parseFloat(document.getElementById('sample1Input').value);
        const maxSampleCount = parseFloat(document.getElementById('sample2Input').value);
        const foldScore = parseFloat(document.getElementById('foldInput').value);
        const foldGroup1 = document.getElementById('group1FoldInput').value;
        const foldGroup2 = document.getElementById('group2FoldInput').value;
        const foldSelectGroup = document.getElementById('selectFoldInput').value;

        // Check if all fold score inputs are filled
        const foldScoreInputsFilled = foldScore && foldGroup1 && foldGroup2 && foldSelectGroup;

        visualizeData(sampleData, false, minScore, maxScore, findFeatureId,
                      minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                      minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                      showOnlyAnnotationFeatures, showOnlyBlankFeatures,
                      minMzScore, maxMzScore, minSampleCount, maxSampleCount,
                      foldScoreInputsFilled ? foldScore : null, foldGroup1, foldGroup2, foldSelectGroup);
        chromatogramElement.on('plotly_click', handleChromatogramClick);

        if (currentBoxParams) {
            addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
        }

        updateRetainedFeatures(minScore, maxScore, findFeatureId,
                               minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                               minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                               showOnlyAnnotationFeatures, showOnlyBlankFeatures,
                               minMzScore, maxMzScore, minSampleCount, maxSampleCount,
                               foldScoreInputsFilled ? foldScore : null, foldGroup1, foldGroup2, foldSelectGroup);
    }

    function updateRetainedFeatures(minScore, maxScore, findFeatureId,
    minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
    minMatchRange, maxMatchRange, showOnlyMatchFeatures,
    showAnnotationFeatures, showBlankFeatures,
    minMzScore, maxMzScore, minSampleScore, maxSampleScore,
    foldScore, foldGroup1, foldGroup2, foldSelectGroup) {
        document.querySelectorAll('.select-sample').forEach(row => {
            const sampleName = row.getAttribute('data-sample-name');
            const sampleData = getSampleData(sampleName, statsChromatogram);
            const featuresWithinRange = getFeaturesWithinRange(sampleData, minScore, maxScore, findFeatureId,
                minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                minMatchRange, maxMatchRange, showOnlyMatchFeatures,
                showAnnotationFeatures, showBlankFeatures,
                minMzScore, maxMzScore, minSampleScore, maxSampleScore,
                foldScore, foldGroup1, foldGroup2, foldSelectGroup);
            row.children[2].textContent = featuresWithinRange;
        });
    }

    initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures,
        sampleData, chromatogramElement, getCurrentBoxParams);
});