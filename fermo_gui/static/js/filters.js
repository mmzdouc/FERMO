export function initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures, sampleData, chromatogramElement, currentBoxParams) {
    const noveltyRange1 = document.getElementById('noveltyRange1');
    const noveltyRange2 = document.getElementById('noveltyRange2');
    const noveltyRange1Input = document.getElementById('noveltyRange1Input');
    const noveltyRange2Input = document.getElementById('noveltyRange2Input');
    const phenotypeRange1 = document.getElementById('phenotypeRange1');
    const phenotypeRange2 = document.getElementById('phenotypeRange2');
    const phenotypeRange1Input = document.getElementById('phenotypeRange1Input');
    const phenotypeRange2Input = document.getElementById('phenotypeRange2Input');
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

    // Event listeners for Novelty score slider
    noveltyRange1.addEventListener('input', () => {
        noveltyRange1Input.value = noveltyRange1.value;
        updateRange();
    });
    noveltyRange2.addEventListener('input', () => {
        noveltyRange2Input.value = noveltyRange2.value;
        updateRange();
    });
    noveltyRange1Input.addEventListener('input', () => {
        noveltyRange1.value = noveltyRange1Input.value;
        updateRange();
    });
    noveltyRange2Input.addEventListener('input', () => {
        noveltyRange2.value = noveltyRange2Input.value;
        updateRange();
    });

    // Event listeners for Phenotype score slider
    phenotypeRange1.addEventListener('input', () => {
        phenotypeRange1Input.value = phenotypeRange1.value;
        updateRange();
    });
    phenotypeRange2.addEventListener('input', () => {
        phenotypeRange2Input.value = phenotypeRange2.value;
        updateRange();
    });
    phenotypeRange1Input.addEventListener('input', () => {
        phenotypeRange1.value = phenotypeRange1Input.value;
        updateRange();
    });
    phenotypeRange2Input.addEventListener('input', () => {
        phenotypeRange2.value = phenotypeRange2Input.value;
        updateRange();
    });

    // Event listener for showPhenotypeFeatures toggle
    showPhenotypeFeatures.addEventListener('change', updateRange);

    function enforceConstraints() {
        if (parseFloat(noveltyRange1Input.value) > parseFloat(noveltyRange2Input.value)) {
            noveltyRange1Input.value = noveltyRange2Input.value;
        }
        if (parseFloat(noveltyRange2Input.value) < parseFloat(noveltyRange1Input.value)) {
            noveltyRange2Input.value = noveltyRange1Input.value;
        }
        if (parseFloat(phenotypeRange1Input.value) > parseFloat(phenotypeRange2Input.value)) {
            phenotypeRange1Input.value = phenotypeRange2Input.value;
        }
        if (parseFloat(phenotypeRange2Input.value) < parseFloat(phenotypeRange1Input.value)) {
            phenotypeRange2Input.value = phenotypeRange1Input.value;
        }
        updateRange();
    }

    // Call updateRange to apply current settings immediately
    updateRange();
}

export function getFeaturesWithinRange(sampleData, minScore, maxScore, minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures) {
    var featuresWithinRange = 0;
    sampleData.novScore.forEach((score, index) => {
        const phenotypeScore = sampleData.annotations?.[index]?.phenotypes?.[0]?.score;
        if (score >= minScore && score <= maxScore &&
            (!showOnlyPhenotypeFeatures || (phenotypeScore !== undefined && phenotypeScore !== null && phenotypeScore >= minPhenotypeScore && phenotypeScore <= maxPhenotypeScore))) {
            featuresWithinRange++;
        }
    });
    return featuresWithinRange;
}

export function getSliderRanges() {
    // Get elements
    const noveltyRange1 = document.getElementById('noveltyRange1');
    const noveltyRange2 = document.getElementById('noveltyRange2');
    const noveltyRange1Input = document.getElementById('noveltyRange1Input');
    const noveltyRange2Input = document.getElementById('noveltyRange2Input');

    // Add event listeners for input events
    noveltyRange1.addEventListener('input', updateRangeFromSlider);
    noveltyRange2.addEventListener('input', updateRangeFromSlider);
    noveltyRange1Input.addEventListener('input', updateRangeFromInput);
    noveltyRange2Input.addEventListener('input', updateRangeFromInput);

    // Add event listeners for blur events to enforce constraints on loss of focus
    noveltyRange1Input.addEventListener('blur', enforceConstraints);
    noveltyRange2Input.addEventListener('blur', enforceConstraints);
}

// Update sliders based on slider input
export function updateRangeFromSlider() {
    const noveltyRange1 = document.getElementById('noveltyRange1');
    const noveltyRange2 = document.getElementById('noveltyRange2');
    const noveltyRange1Input = document.getElementById('noveltyRange1Input');
    const noveltyRange2Input = document.getElementById('noveltyRange2Input');

    const minRange = Math.min(parseFloat(noveltyRange1.value), parseFloat(noveltyRange2.value));
    const maxRange = Math.max(parseFloat(noveltyRange1.value), parseFloat(noveltyRange2.value));

    noveltyRange1.value = minRange;
    noveltyRange2.value = maxRange;

    noveltyRange1Input.value = minRange.toFixed(2);
    noveltyRange2Input.value = maxRange.toFixed(2);
}

// Update sliders based on input field values
export function updateRangeFromInput() {
    const noveltyRange1 = document.getElementById('noveltyRange1');
    const noveltyRange2 = document.getElementById('noveltyRange2');
    const noveltyRange1Input = document.getElementById('noveltyRange1Input');
    const noveltyRange2Input = document.getElementById('noveltyRange2Input');

    const minRange = parseFloat(noveltyRange1Input.value);
    const maxRange = parseFloat(noveltyRange2Input.value);

    if (!isNaN(minRange) && !isNaN(maxRange)) {
        noveltyRange1.value = minRange;
        noveltyRange2.value = maxRange;
    }
}

// Enforce constraints when the input fields lose focus
export function enforceConstraints() {
    const noveltyRange1 = document.getElementById('noveltyRange1');
    const noveltyRange2 = document.getElementById('noveltyRange2');
    const noveltyRange1Input = document.getElementById('noveltyRange1Input');
    const noveltyRange2Input = document.getElementById('noveltyRange2Input');

    let minRange = parseFloat(noveltyRange1Input.value);
    let maxRange = parseFloat(noveltyRange2Input.value);

    if (isNaN(minRange)) {
        minRange = 0;
    }
    if (isNaN(maxRange)) {
        maxRange = 1;
    }

    minRange = Math.max(0, Math.min(minRange, 1));
    maxRange = Math.max(0, Math.min(maxRange, 1));

    if (minRange > maxRange) {
        [minRange, maxRange] = [maxRange, minRange];
    }

    noveltyRange1.value = minRange;
    noveltyRange2.value = maxRange;

    noveltyRange1Input.value = minRange.toFixed(2);
    noveltyRange2Input.value = maxRange.toFixed(2);
}