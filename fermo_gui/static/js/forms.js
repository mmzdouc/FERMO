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


function toggleGenericModule(element_id, class_selector) {
    var choice = document.getElementById(element_id).value;
    if (choice === 'True') {
        toggleShow(class_selector);
    } else {
        toggleHide(class_selector);
    }
}

function togglePhenotypeFormat() {
    var choice = document.getElementById('phenotype_format').value;
    if (choice === 'qualitative') {
        toggleShow(".phenotype-qualitative");
        toggleHide(".phenotype-quantitative");
    } else if (choice === '') {
        toggleHide(".phenotype-quantitative");
        toggleHide(".phenotype-qualitative");
    } else {
        toggleShow(".phenotype-quantitative");
        toggleHide(".phenotype-qualitative");
    }
}

window.onload = function() {
    document.getElementById('peaktable_filter_toggle').addEventListener('change', function() {
        toggleGenericModule('peaktable_filter_toggle', '.peaktable-filter');
    });
    document.getElementById('msms_cosine_toggle').addEventListener('change', function() {
        toggleGenericModule('msms_cosine_toggle', '.msms-cosine');
    });
    document.getElementById('msms_deepscore_toggle').addEventListener('change', function() {
        toggleGenericModule('msms_deepscore_toggle', '.msms-deepscore');
    });
    document.getElementById('group_blank_toggle').addEventListener('change', function() {
        toggleGenericModule('group_blank_toggle', '.group-blank');
    });
    document.getElementById('group_factor_toggle').addEventListener('change', function() {
        toggleGenericModule('group_factor_toggle', '.group-factor');
    });
    document.getElementById('phenotype_format').addEventListener('change', togglePhenotypeFormat);
    document.getElementById('library_cosine_toggle').addEventListener('change', function() {
        toggleGenericModule('library_cosine_toggle', '.library-cosine');
    });
    document.getElementById('library_deepscore_toggle').addEventListener('change', function() {
        toggleGenericModule('library_deepscore_toggle', '.library-deepscore');
    });
    document.getElementById('askcb_cosine_toggle').addEventListener('change', function() {
        toggleGenericModule('askcb_cosine_toggle', '.askcb-cosine');
    });
    document.getElementById('askcb_deepscore_toggle').addEventListener('change', function() {
        toggleGenericModule('askcb_deepscore_toggle', '.askcb-deepscore');
    });
};
