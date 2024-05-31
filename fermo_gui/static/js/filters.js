
export function getSliderRanges() {
    // Get elements
    const range1 = document.getElementById('range1');
    const range2 = document.getElementById('range2');
    const range1Input = document.getElementById('range1Input');
    const range2Input = document.getElementById('range2Input');

    // Add event listeners for input events
    range1.addEventListener('input', updateRangeFromSlider);
    range2.addEventListener('input', updateRangeFromSlider);
    range1Input.addEventListener('input', updateRangeFromInput);
    range2Input.addEventListener('input', updateRangeFromInput);

    // Add event listeners for blur events to enforce constraints on loss of focus
    range1Input.addEventListener('blur', enforceConstraints);
    range2Input.addEventListener('blur', enforceConstraints);
}

// Update sliders based on slider input
export function updateRangeFromSlider() {
    const minRange = Math.min(parseFloat(range1.value), parseFloat(range2.value));
    const maxRange = Math.max(parseFloat(range1.value), parseFloat(range2.value));

    range1.value = minRange;
    range2.value = maxRange;

    range1Input.value = minRange.toFixed(2);
    range2Input.value = maxRange.toFixed(2);
}

// Update sliders based on input field values
export function updateRangeFromInput() {
    const minRange = parseFloat(range1Input.value);
    const maxRange = parseFloat(range2Input.value);

    if (!isNaN(minRange) && !isNaN(maxRange)) {
        range1.value = minRange;
        range2.value = maxRange;
    }
}

// Enforce constraints when the input fields lose focus
export function enforceConstraints() {
    let minRange = parseFloat(range1Input.value);
    let maxRange = parseFloat(range2Input.value);

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

    range1.value = minRange;
    range2.value = maxRange;

    range1Input.value = minRange.toFixed(2);
    range2Input.value = maxRange.toFixed(2);
}
