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
    // add event listener to the form which handles the submit
    filterForm.addEventListener('submit', function(evt) {
        evt.preventDefault()
        if (document.valuesChanged) { // only submit if values were changed
            let formData = new FormData(filterForm)
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
                        console.log('fetched data in filterPanel.js', data)
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
