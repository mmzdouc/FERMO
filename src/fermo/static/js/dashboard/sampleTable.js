/**
 * Make rows selectable and change pointer to hand when hovering
 */
export function selectRows(){
    const allRows = document.querySelectorAll('#selectSample tr')

    for (let i=1; i<allRows.length; i++){
        // get sample identifier (i.e. the filename of each sample)
        const sample = allRows[i].innerText.split('\t')[0]

        // set an attribute 'data-value' for each row to its sample name
        allRows[i].setAttribute('data-value', sample) 

        // add clickEvent listener to each row
        allRows[i].addEventListener('click', function(e){
            const sampleName = this.getAttribute('data-value')
            console.log('data-value:', sampleName)
            console.log('window.location:', window.location.href)
            fetch(window.location.href, { // send POST request to current URL
                method: 'POST',
                body: JSON.stringify({sample: sampleName}),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
        })

        // change mouse pointer to a hand when hovering over a row
        allRows[i].addEventListener('mouseover', function(e){
            this.style.cursor='pointer'
        })
    }
}
