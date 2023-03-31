// code until line 87 was taken and adjusted from https://medium.com/@predragdavidovic10/native-dual-range-slider-html-css-javascript-91e778134816

function controlFromInput(fromSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#116789', controlSlider);
    if (from > to) {
        fromSlider.value = to;
        fromInput.value = to;
    } else {
        fromSlider.value = from;
    }
}

function controlToInput(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#116789', controlSlider);
    setToggleAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}

function controlFromSlider(fromSlider, toSlider, fromInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#116789', toSlider);
  if (from > to) {
    fromSlider.value = to;
    fromInput.value = to;
  } else {
    fromInput.value = from;
  }
}

function controlToSlider(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#116789', toSlider);
  setToggleAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}

function getParsed(currentFrom, currentTo) {
  const from = parseFloat(currentFrom.value);
  const to = parseFloat(currentTo.value);
  return [from, to];
}

/**
 * Control coloring of the slider depending on the selected range
* @param {string} fromSlider    - HTML-ID of the slider that controls the lower bound
* @param {string} toSlider      - HTML-ID of the slider that controls the upper bound
* @param {string} sliderColor   - Hexcode for the color of the unselected part of the slider
* @param {string} rangeColor    - Hexcode for the color of the selected range
* @param {string} controlSlider - same as toSlider but necessary to prevent background-color-on-input-field bug
 */
function fillSlider(fromSlider, toSlider, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = (toSlider.max-toSlider.min) / toSlider.step;
    const fromPosition = (fromSlider.value - toSlider.min) / toSlider.step;
    const toPosition = (toSlider.value - toSlider.min) / toSlider.step;
    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
      ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
      ${rangeColor} ${(toPosition)/(rangeDistance)*100}%,
      ${sliderColor} ${(toPosition)/(rangeDistance)*100}%,
      ${sliderColor} 100%)`;
}

/**
 * Keep 'toSlider' at the bottom of the stack when the two sliders overlap
 * to avoid interferance with the input elements
*/
function setToggleAccessible(currentTarget) {
  if (Number(currentTarget.value) <= 0 ) {
    currentTarget.style.zIndex = 2;
  } else {
    currentTarget.style.zIndex = 0;
  }
}

/**
 * Check if script was called from desired page and return boolean value
 * 
 * @param {string} desiredPage - Name of the desired page (return true if script was called from this page)
*/
function checkURL(desiredPage) {
  var pageurl = window.location.href; // get the URL of the current page
  var splitUrl = pageurl.split("/");
  var currentPage = (splitUrl[splitUrl.length - 1]); // access last element of the URL
  if (desiredPage == currentPage) /*check whether the current page is {pagename}*/
  {
    return true;
  } else {
    return false;
  }
}

/**
 * Initialize the multi-range-Slider 
 * @param {string} fromSliderID - HTML-ID of the slider that controls the lower bound
 * @param {string} toSliderID   - HTML-ID of the slider that controls the upper bound
 * @param {string} fromInputID  - HTML-ID of the input element that controls the lower bound
 * @param {string} toInputID    - HTML-ID of the input element that controls the upper bound
*/
function initSlider(fromSliderID, toSliderID, fromInputID, toInputID) {
  const fromSlider = document.querySelector(fromSliderID);
  const toSlider = document.querySelector(toSliderID);
  const fromInput = document.querySelector(fromInputID);
  const toInput = document.querySelector(toInputID);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#116789', toSlider);
  setToggleAccessible(toSlider);

  fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider, fromInput);
  toSlider.oninput = () => controlToSlider(fromSlider, toSlider, toInput);
  fromInput.oninput = () => controlFromInput(fromSlider, fromInput, toInput, toSlider);
  toInput.oninput = () => controlToInput(toSlider, fromInput, toInput, toSlider);
}




// Call functions with correct parameters depending on the page it was called from
if(checkURL("processing")){

  // Slider for relative intensity filter (processing page)
  initSlider('#fromSlider', '#toSlider', '#fromInput', '#toInput');

  // Slider for MS2Query relative intensity filter (processing page)
  initSlider('#fromSliderMS2Q', '#toSliderMS2Q', '#fromInputMS2Q', '#toInputMS2Q');

} else if (checkURL("dashboard")){

  // Slider for Novelty Score (dashboard page)
  initSlider('#fromSliderNovel', '#toSliderNovel', '#fromInputNovel', '#toInputNovel');

  // Slider for Relative intensity (dashboard page)
  initSlider('#fromSliderRelInt', '#toSliderRelInt', '#fromInputRelInt', '#toInputRelInt');

  // Slider for Peak overlap (dashboard page)
  initSlider('#fromSliderPeak', '#toSliderPeak', '#fromInputPeak', '#toInputPeak');
}
