function toggleDisplay(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
    if (el.classList.contains('d-none')) {
      el.classList.remove('d-none');
      el.classList.add('d-block');
    } else {
      el.classList.remove('d-block');
      el.classList.add('d-none');
    }
   });
}

function toggleDisplayMsms() {
  toggleDisplay('#msms');
}

function toggleDisplayPhenotype() {
  toggleDisplay('#phenotype');
}


function toggleShow(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
    if (el.classList.contains('d-none')) {
      el.classList.remove('d-none');
      el.classList.add('d-block');
    } else {
      // pass
    }
   });
}

function toggleHide(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
    if (el.classList.contains('d-block')) {
      el.classList.remove('d-block');
      el.classList.add('d-none');
    } else {
      // pass
    }
   });
}

function togglePhenotypeFormat() {
    var choice = document.getElementById('phenotype_format').value;
    if (choice === 'qualitative') {
        toggleShow("#phenotype-qualit");
        toggleHide("#phenotype-quant");
    } else if (choice === '') {
        toggleHide("#phenotype-quant");
        toggleHide("#phenotype-qualit");
    } else {
        toggleShow("#phenotype-quant");
        toggleHide("#phenotype-qualit");
    }
}

function togglePeaktableFilter() {
    var choice = document.getElementById('peaktable_filter_toggle').value;
    if (choice === 'True') {
        toggleShow("#peaktable-filter");
    } else {
        toggleHide("#peaktable-filter");
    }
}

window.onload = function() {
    document.getElementById('peaktable_filter_toggle').addEventListener('change', togglePeaktableFilter);
    document.getElementById('phenotype_format').addEventListener('change', togglePhenotypeFormat);
};
