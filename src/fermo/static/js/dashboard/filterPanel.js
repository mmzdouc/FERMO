import { plotMainChromatogram } from './chromatogram.js'
import { updateTable } from './featureTable.js'
import { selectRows } from './sampleTable.js'

/**
 * Add event listeners to the form and its input elements
 */
export function filterFeatures() {
    const filterForm = document.getElementById('featureVisibility').parentNode
    let inputElems = filterForm.querySelectorAll('input')
    document.valuesChanged = false

    // add event listeners to all input elements
    for (let i = 0; i < inputElems.length; i++) {
        inputElems[i].addEventListener('change', function(evt) {
            document.valuesChanged = true
        })

        inputElems[i].addEventListener('focusout', function(evt) {
            inputElems = Array.from(inputElems)
            let actvElem = evt.relatedTarget
            if (inputElems.includes(actvElem)) {
                // pass
                // i.e. do not submit, when user clicks on another input element
            }
            else { // submit the form
                filterForm.requestSubmit()
                document.valuesChanged = false
            }
        })
    }
    // add event listener which handles the submit to the form
    filterForm.addEventListener('submit', function(evt) {
        evt.preventDefault()
        if (document.valuesChanged) { // only submit if values were changed
            let formData = new FormData(filterForm)
            /* sending as regular form data causes an error with flask,
             so use json as workaround */
            formData = JSON.stringify(Object.fromEntries(formData))
            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: new Headers({
                    'Content-Type': 'application/json' 
                })
            })
            .then(function (response) {
                if (response.ok) {
                    response.json()
                    .then(function (data) {
                        const chromatogram = JSON.parse(data.chromatogram)
                        const sampleStatsList = JSON.parse(data.sample_stats_table)
                        const sampleOverviewList = JSON.parse(data.sample_overview_table)


                        plotMainChromatogram(chromatogram)
                        updateTable(sampleStatsList, '#generalSampleTable tbody')
                        updateTable(sampleOverviewList, '#sampleOverviewTable tbody')
                        selectRows()  // reinitialize event listeners for sample table
                    })
                } else {
                    console.log(
                        `fetch was not successfull: ${response.status}`
                    )
                    return ;
                }
            })
        }
    })
}
