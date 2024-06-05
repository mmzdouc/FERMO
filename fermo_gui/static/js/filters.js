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
        findFId: document.getElementById('findInput'),
        mz1Input: document.getElementById('mz1Input'),
        mz2Input: document.getElementById('mz2Input'),
        sample1Input: document.getElementById('sample1Input'),
        sample2Input: document.getElementById('sample2Input'),
        foldInput: document.getElementById('foldInput'),
        group1FoldInput: document.getElementById('group1FoldInput'),
        group2FoldInput: document.getElementById('group2FoldInput'),
        selectFoldInput: document.getElementById('selectFoldInput')
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
        const minMzScore = parseFloat(elements.mz1Input.value);
        const maxMzScore = parseFloat(elements.mz2Input.value);
        const minSampleCount = parseFloat(elements.sample1Input.value);
        const maxSampleCount = parseFloat(elements.sample2Input.value);
        const foldScore = parseFloat(elements.foldInput.value);
        const foldGroup1 = elements.group1FoldInput.value;
        const foldGroup2 = elements.group2FoldInput.value;
        const foldSelectGroup = elements.selectFoldInput.value;

        visualizeData(sampleData, false, minScore, maxScore, findFeatureId,
                      minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                      minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                      showOnlyAnnotationFeatures, showOnlyBlankFeatures,
                      minMzScore, maxMzScore, minSampleCount, maxSampleCount,
                      foldScore, foldGroup1, foldGroup2, foldSelectGroup);
        chromatogramElement.on('plotly_click', handleChromatogramClick);

        const currentBoxParams = getCurrentBoxParams();
        if (currentBoxParams) {
            addBoxVisualization(currentBoxParams.traceInt, currentBoxParams.traceRt);
        }
        updateRetainedFeatures(minScore, maxScore, findFeatureId,
                               minPhenotypeScore, maxPhenotypeScore, showOnlyPhenotypeFeatures,
                               minMatchScore, maxMatchScore, showOnlyMatchFeatures,
                               showOnlyAnnotationFeatures, showOnlyBlankFeatures,
                               minMzScore, maxMzScore, minSampleCount, maxSampleCount,
                               foldScore, foldGroup1, foldGroup2, foldSelectGroup);
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
                                       showOnlyAnnotationFeatures, showOnlyBlankFeatures,
                                       minMzScore, maxMzScore, minSampleCount, maxSampleCount,
                                       foldScore, foldGroup1, foldGroup2, foldSelectGroup) {
    return sampleData.novScore.reduce((count, score, index) => {
        const phenotypeScore = sampleData.annotations?.[index]?.phenotypes?.[0]?.score;
        const matchScore = sampleData.annotations?.[index]?.matches?.[0]?.score;
        const annotation = sampleData.annotations?.[index]?.adducts ?? null;
        const mz = sampleData.precMz[index];
        const blanks = sampleData.blankAs?.[index];
        const findFeature = sampleData.featureId?.[index];
        const sampleCount = sampleData.samples[index].length;
        const foldChanges = sampleData.fGroupData?.[index]?.[foldSelectGroup] ?? [];

        // Check fold change conditions
        let foldValid = !foldScore || !foldGroup1 || !foldGroup2 || !foldSelectGroup;
        if (!foldValid) {
            for (const foldChange of foldChanges) {
                if ((foldChange.group1 === foldGroup1 && foldChange.group2 === foldGroup2) ||
                    (foldChange.group1 === foldGroup2 && foldChange.group2 === foldGroup1)) {
                    if (foldChange.factor >= foldScore) {
                        foldValid = true;
                        break;
                    }
                }
            }
        }

        if (score >= minScore && score <= maxScore &&
            (!showOnlyPhenotypeFeatures || (phenotypeScore !== null &&
            phenotypeScore >= minPhenotypeScore && phenotypeScore <= maxPhenotypeScore)) &&
            (!showOnlyMatchFeatures || (matchScore !== null &&
            matchScore >= minMatchScore && matchScore <= maxMatchScore)) &&
            (!showOnlyAnnotationFeatures || (annotation !== null)) &&
            (!showOnlyBlankFeatures || (blanks !== true)) &&
            (!findFeatureId || (findFeatureId === findFeature)) &&
            (!maxMzScore || (mz >= minMzScore && mz <= maxMzScore)) &&
            (!maxSampleCount || (sampleCount >= minSampleCount && sampleCount <= maxSampleCount)) &&
            foldValid
            ) {
            return count + 1;
        }
        return count;
    }, 0);
}

export function getFilterGroupSelectionFields(statsGroups) {
    const selectFoldInput = document.getElementById('selectFoldInput');
    const group1FoldInput = document.getElementById('group1FoldInput');
    const group2FoldInput = document.getElementById('group2FoldInput');

    // Populate selectFoldInput
    selectFoldInput.innerHTML = '<option value="null" selected>select group</option>';
    Object.keys(statsGroups).forEach(groupKey => {
        const option = document.createElement('option');
        option.value = groupKey;
        option.textContent = groupKey;
        selectFoldInput.appendChild(option);
    });

    // Event listener for selectFoldInput
    selectFoldInput.addEventListener('change', () => {
        const selectedGroup = selectFoldInput.value;
        if (selectedGroup !== "null") {
            const groupValues = statsGroups[selectedGroup];

            // Populate group1FoldInput
            group1FoldInput.innerHTML = '<option value="" selected>group 1</option>';
            groupValues.forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                group1FoldInput.appendChild(option);
            });

            // Populate group2FoldInput
            group2FoldInput.innerHTML = '<option value="" selected>group 2</option>';
            groupValues.forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                group2FoldInput.appendChild(option);
            });

            // Enable the select inputs
            group1FoldInput.disabled = false;
            group2FoldInput.disabled = false;
        } else {
            // Clear and disable the select inputs if no group is selected
            group1FoldInput.innerHTML = '<option value="" selected>group 1</option>';
            group2FoldInput.innerHTML = '<option value="" selected>group 2</option>';
            group1FoldInput.disabled = true;
            group2FoldInput.disabled = true;
        }
    });

    // Initially disable the select inputs
    group1FoldInput.disabled = true;
    group2FoldInput.disabled = true;
}