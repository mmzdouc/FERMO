import { getSampleData, getFeatureData } from './parsing.js';
import { updateFeatureTables, hideTables } from './dynamic_tables.js';
import { visualizeData } from './chromatogram.js';
import { hideNetwork } from './network.js';

document.addEventListener('DOMContentLoaded', function() {
    var dragged;

    // Drag and Drop functionality
    document.addEventListener("drag", function(event) {}, false);

    document.addEventListener("dragstart", function(event) {
        dragged = event.target;
        // make it half transparent
        event.target.style.opacity = .5;
        event.dataTransfer.setData("draggedAccId", event.target.id);
        setTimeout(() => event.target.classList.toggle("hidden"));
        // change dropzone background when hovering
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "#a3a3a3";
        }
        // highlight dropzones
        document.querySelectorAll('.dropzone').forEach(function(dropzone) {
            dropzone.classList.add('dropzone-dragging');
        });
    }, false);

    document.addEventListener("dragend", function(event) {
        // reset the transparency
        event.target.style.opacity = "";
        // reset dropzone background
        document.querySelectorAll('.dropzone').forEach(function(dropzone) {
            dropzone.classList.remove('dropzone-dragging');
        });
    }, false);

    document.addEventListener("dragover", function(event) {
        // prevent default to allow drop
        event.preventDefault();
    }, false);

    document.addEventListener("dragenter", function(event) {
        // highlight potential drop target when the draggable element enters it
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "#a3a3a3";
        }
    }, false);

    document.addEventListener("dragleave", function(event) {
        // reset background of potential drop target when the draggable element leaves it
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "";
        }
    }, false);

    document.addEventListener("drop", function(event) {
        event.preventDefault();

        // move dragged elem to the selected drop target
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "";

            // Get the ID of the dragged accordion from the data transfer object
            const draggedAccId = event.dataTransfer.getData("draggedAccId");
            const draggedAcc = document.getElementById(draggedAccId);
            const fromContainer = draggedAcc.parentNode;
            const toContainer = event.target;

            // Check if the drop zone is already occupied, if so swap containers, if not append
            if (toContainer !== fromContainer) {
                const existingAcc = toContainer.firstElementChild;
                if (existingAcc) {
                    fromContainer.appendChild(existingAcc);
                }
                toContainer.appendChild(draggedAcc);
            } else {
                toContainer.appendChild(draggedAcc);
            }
        }
    }, false);

    // Load all chromatogram data
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

        // Update the feature table on chromatogram click
        chromatogramElement.on('plotly_click', function(data) {
            var featureId = data.points[0].data.name;
            updateFeatureTables(featureId, sampleData, statsNetwork);
        });
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

            // Update the feature table on chromatogram click
            chromatogramElement.on('plotly_click', function(data) {
                var featureId = data.points[0].data.name;
                updateFeatureTables(featureId, sampleData, statsNetwork);
            });
        });
    });
});