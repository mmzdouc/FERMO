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
        toggleShow(".phenotype-qualitative");
        toggleHide(".phenotype-quantitative-perc");
        toggleHide(".phenotype-quantitative-conc");
    } else if (choice === 'quantitative-percentage') {
        toggleHide(".phenotype-qualitative");
        toggleShow(".phenotype-quantitative-perc");
        toggleHide(".phenotype-quantitative-conc");
    } else if (choice === 'quantitative-concentration') {
        toggleHide(".phenotype-qualitative");
        toggleHide(".phenotype-quantitative-perc");
        toggleShow(".phenotype-quantitative-conc");
    } else {
        toggleHide(".phenotype-qualitative");
        toggleHide(".phenotype-quantitative-perc");
        toggleHide(".phenotype-quantitative-conc");
    }
}

window.onload = function() {
    document.getElementById('phenotype_format').addEventListener('change', togglePhenotypeFormat);
};
