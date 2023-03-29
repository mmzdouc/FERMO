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
  if (pagename == pgname) /*check whether the current page is {pagename} or not*/
  {
    return true;
  } else {
    return false;
  }
}


// call functions with correct parameters depending on the page it was called from
if(checkURL("processing")){
  // Slider for relative intensity filter (processing page)
  const fromSlider = document.querySelector('#fromSlider');
  const toSlider = document.querySelector('#toSlider');
  const fromInput = document.querySelector('#fromInput');
  const toInput = document.querySelector('#toInput');
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#116789', toSlider);
  setToggleAccessible(toSlider);

  fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider, fromInput);
  toSlider.oninput = () => controlToSlider(fromSlider, toSlider, toInput);
  fromInput.oninput = () => controlFromInput(fromSlider, fromInput, toInput, toSlider);
  toInput.oninput = () => controlToInput(toSlider, fromInput, toInput, toSlider);

  // Slider for MS2Query relative intensity filter (processing page)
  const fromSliderMS2Q = document.querySelector('#fromSliderMS2Q');
  const toSliderMS2Q = document.querySelector('#toSliderMS2Q');
  const fromInputMS2Q = document.querySelector('#fromInputMS2Q');
  const toInputMS2Q = document.querySelector('#toInputMS2Q');
  fillSlider(fromSliderMS2Q, toSliderMS2Q, '#C6C6C6', '#116789', toSliderMS2Q);
  setToggleAccessible(toSliderMS2Q);

  fromSliderMS2Q.oninput = () => controlFromSlider(fromSliderMS2Q, toSliderMS2Q, fromInputMS2Q);
  toSliderMS2Q.oninput = () => controlToSlider(fromSliderMS2Q, toSliderMS2Q, toInputMS2Q);
  fromInputMS2Q.oninput = () => controlFromInput(fromSliderMS2Q, fromInputMS2Q, toInputMS2Q, toSliderMS2Q);
  toInputMS2Q.oninput = () => controlToInput(toSliderMS2Q, fromInputMS2Q, toInputMS2Q, toSliderMS2Q);

} else if (checkURL("dashboard")){

  // Slider for Novelty Score (dashboard page)
  const fromSliderNovel = document.querySelector('#fromSliderNovel');
  const toSliderNovel = document.querySelector('#toSliderNovel');
  const fromInputNovel = document.querySelector('#fromInputNovel');
  const toInputNovel = document.querySelector('#toInputNovel');
  fillSlider(fromSliderNovel, toSliderNovel, '#C6C6C6', '#116789', toSliderNovel);
  setToggleAccessible(toSliderNovel);

  fromSliderNovel.oninput = () => controlFromSlider(fromSliderNovel, toSliderNovel, fromInputNovel);
  toSliderNovel.oninput = () => controlToSlider(fromSliderNovel, toSliderNovel, toInputNovel);
  fromInputNovel.oninput = () => controlFromInput(fromSliderNovel, fromInputNovel, toInputNovel, toSliderNovel);
  toInputNovel.oninput = () => controlToInput(toSliderNovel, fromInputNovel, toInputNovel, toSliderNovel);

  // slider for Relative intensity (dashboard page)
  const fromSliderRelInt = document.querySelector('#fromSliderRelInt');
  const toSliderRelInt = document.querySelector('#toSliderRelInt');
  const fromInputRelInt = document.querySelector('#fromInputRelInt');
  const toInputRelInt = document.querySelector('#toInputRelInt');
  fillSlider(fromSliderRelInt, toSliderRelInt, '#C6C6C6', '#116789', toSliderRelInt);
  setToggleAccessible(toSliderRelInt);

  fromSliderRelInt.oninput = () => controlFromSlider(fromSliderRelInt, toSliderRelInt, fromInputRelInt);
  toSliderRelInt.oninput = () => controlToSlider(fromSliderRelInt, toSliderRelInt, toInputRelInt);
  fromInputRelInt.oninput = () => controlFromInput(fromSliderRelInt, fromInputRelInt, toInputRelInt, toSliderRelInt);
  toInputRelInt.oninput = () => controlToInput(toSliderRelInt, fromInputRelInt, toInputRelInt, toSliderRelInt);

  // slider for Peak overlap (dashboard page)
  const fromSliderPeak = document.querySelector('#fromSliderPeak');
  const toSliderPeak = document.querySelector('#toSliderPeak');
  const fromInputPeak = document.querySelector('#fromInputPeak');
  const toInputPeak = document.querySelector('#toInputPeak');
  fillSlider(fromSliderPeak, toSliderPeak, '#C6C6C6', '#116789', toSliderPeak);
  setToggleAccessible(toSliderPeak);

  fromSliderPeak.oninput = () => controlFromSlider(fromSliderPeak, toSliderPeak, fromInputPeak);
  toSliderPeak.oninput = () => controlToSlider(fromSliderPeak, toSliderPeak, toInputPeak);
  fromInputPeak.oninput = () => controlFromInput(fromSliderPeak, fromInputPeak, toInputPeak, toSliderPeak);
  toInputPeak.oninput = () => controlToInput(toSliderPeak, fromInputPeak, toInputPeak, toSliderPeak);
}

