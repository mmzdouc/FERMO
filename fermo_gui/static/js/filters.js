export function initializeFilters(visualizeData, handleChromatogramClick, addBoxVisualization, updateRetainedFeatures,
                                  sampleData, chromatogramElement, getCurrentBoxParams) {
    const elements = {
        noveltyRange1: document.getElementById('noveltyRange1'),
        noveltyRange2: document.getElementById('noveltyRange2'),
        noveltyRange1Input: document.getElementById('noveltyRange1Input'),
        noveltyRange2Input: document.getElementById('noveltyRange2Input'),
        phenotypeRange1: document.getElementById('phenotypeRange1'),
        phenotypeRange2: document.getElementById('phenotypeRange2'),
        phenotypeRange1Input: document.getElementById('phenotypeRange1Input'),
        phenotypeRange2Input: document.getElementById('phenotypeRange2Input'),
        showPhenotypeFeatures: document.getElementById('showPhenotypeFeatures'),
        matchRange1: document.getElementById('matchRange1'),
        matchRange2: document.getElementById('matchRange2'),
        matchRange1Input: document.getElementById('matchRange1Input'),
        matchRange2Input: document.getElementById('matchRange2Input'),
        showMatchFeatures: document.getElementById('showMatchFeatures'),
        showAnnotationFeatures: document.getElementById('showAnnotationFeatures'),
        showBlankFeatures: document.getElementById('showBlankFeatures'),
        findFId: document.getElementById('findInput')
    };

    function updateRange() {
        const minScore = parseFloat(elements.noveltyRange1.value);
        const maxScore = parseFloat(elements.noveltyRange2.value);
        const minPhenotypeScore = parseFloat(elements.phenotypeRange1.value);
        const maxPhenotypeScore = parseFloat(elements.phenotypeRange2.value);
        const showOnlyPhenotypeFeatures = elements.showPhenotypeFeatures.checked;
        const minMatchScore = parseFloat(elements.matchRange1.value);
        const maxMatchScore = parseFloat(elements.matchRange2.value);
        const showOnlyMatchFeatures = elements.showMatchFeatures.checked;
        const showOnlyAnnotationFeatures = elements.showAnnotationFeatures.checked;
        const showOnlyBlankFeatures = elements.showBlankFeatures.checked;
        const findFeatureId = parseFloat(elements.findFId.value);

        visualizeData(sampleData, false, minScore, maxScore, findFeatureId,
                      minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                      minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                      showOnlyAnnotationFeatures, showOnlyBlankFeatures);
        chromatogramElement.on('plotly_click', handleChromatogramClick);

        const currentBoxParams = getCurrentBoxParams();
        if (currentBoxParams) {
            addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
        }
        updateRetainedFeatures(minScore, maxScore, findFeatureId,
                               minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                               minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                               showOnlyAnnotationFeatures, showOnlyBlankFeatures);
    }

    function enforceConstraints() {
        if (parseFloat(elements.noveltyRange1Input.value) > parseFloat(elements.noveltyRange2Input.value)) {
            elements.noveltyRange1Input.value = elements.noveltyRange2Input.value;
        }
        if (parseFloat(elements.noveltyRange2Input.value) < parseFloat(elements.noveltyRange1Input.value)) {
            elements.noveltyRange2Input.value = elements.noveltyRange1Input.value;
        }
        if (parseFloat(elements.phenotypeRange1Input.value) > parseFloat(elements.phenotypeRange2Input.value)) {
            elements.phenotypeRange1Input.value = elements.phenotypeRange2Input.value;
        }
        if (parseFloat(elements.phenotypeRange2Input.value) < parseFloat(elements.phenotypeRange1Input.value)) {
            elements.phenotypeRange2Input.value = elements.phenotypeRange1Input.value;
        }
        if (parseFloat(elements.matchRange1Input.value) > parseFloat(elements.matchRange2Input.value)) {
            elements.matchRange1Input.value = elements.matchRange2Input.value;
        }
        if (parseFloat(elements.matchRange2Input.value) < parseFloat(elements.matchRange1Input.value)) {
            elements.matchRange2Input.value = elements.matchRange1Input.value;
        }
        updateRange();
    }

    const rangeElements = [
        { slider: elements.noveltyRange1, input: elements.noveltyRange1Input },
        { slider: elements.noveltyRange2, input: elements.noveltyRange2Input },
        { slider: elements.phenotypeRange1, input: elements.phenotypeRange1Input },
        { slider: elements.phenotypeRange2, input: elements.phenotypeRange2Input },
        { slider: elements.matchRange1, input: elements.matchRange1Input },
        { slider: elements.matchRange2, input: elements.matchRange2Input }
    ];

    rangeElements.forEach(({ slider, input }) => {
        slider.addEventListener('input', () => {
            input.value = slider.value;
            updateRange();
        });
        input.addEventListener('input', () => {
            slider.value = input.value;
            updateRange();
        });
        input.addEventListener('blur', enforceConstraints);
    });

    elements.showPhenotypeFeatures.addEventListener('change', updateRange);
    elements.showMatchFeatures.addEventListener('change', updateRange);

    updateRange();
}

export function getFeaturesWithinRange(sampleData, minScore, maxScore, findFeatureId,
                                       minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                                       minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                                       showOnlyAnnotationFeatures, showOnlyBlankFeatures) {
    return sampleData.novScore.reduce((count, score, index) => {
        const phenotypeScore = sampleData.annotations?.[index]?.phenotypes?.[0]?.score;
        const matchScore = sampleData.annotations?.[index]?.matches?.[0]?.score;
        const annotation = sampleData.annotations?.[index]?.adducts ?? null;
        const blanks = sampleData.blankAs?.[index];
        const findFeature = sampleData.featureId?.[index];
        if (score >= minScore && score <= maxScore &&
            (!showOnlyPhenotypeFeatures || (phenotypeScore !== null &&
            phenotypeScore >= minPhenotypeScore && phenotypeScore <= maxPhenotypeScore)) &&
            (!showOnlyMatchFeatures || (matchScore !== null &&
            matchScore >= minMatchScore && matchScore <= maxMatchScore)) &&
            (!showOnlyAnnotationFeatures || (annotation !== null)) &&
            (!showOnlyBlankFeatures || (blanks !== true)) &&
            (!findFeatureId || (findFeatureId === findFeature))
            ) {
            return count + 1;
        }
        return count;
    }, 0);
}