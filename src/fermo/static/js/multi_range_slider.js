// code taken and adjusted from https://medium.com/@predragdavidovic10/native-dual-range-slider-html-css-javascript-91e778134816

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

function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = (to.max-to.min) / to.step;
    const fromPosition = (from.value - to.min) / to.step;
    const toPosition = (to.value - to.min) / to.step;
    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
      ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
      ${rangeColor} ${(toPosition)/(rangeDistance)*100}%,
      ${sliderColor} ${(toPosition)/(rangeDistance)*100}%,
      ${sliderColor} 100%)`;
}

function setToggleAccessible(currentTarget) {
  /**Keep toSlider at the bottom of the 'stack' when the two sliders overlap
   * to avoid interferance with the input elements */
  if (Number(currentTarget.value) <= 0 ) {
    currentTarget.style.zIndex = 2;
  } else {
    currentTarget.style.zIndex = 0;
  }
}

function checkURL(pagename) {
  /** Check from which URL the script was called */
  var pageurl = window.location.href;
  var pg = pageurl.split("/");
  var pgname = (pg[pg.length - 1]); // access last element of the URL
  if (pagename == pgname) /*check whether the current page is {pagename}*/
  {
    return true;
  } else {
    return false;
  }
}

function initSlider(fromSliderID, toSliderID, fromInputID, toInputID) {
  /** Initialize the multi-range-Slider */
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


// call functions with correct parameters depending on the page it was called from
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
