import { plotChromatogram } from './chromatogram.js';

/**
 * Make rows selectable and change pointer to hand when hovering over a row.
 * Call plotChromatogram() when a row is clicked.
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

            // send POST request to current URL
            fetch(window.location.href, {
                method: 'POST',
                body: JSON.stringify({sample: sampleName}),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
            // define what to do with the response
            .then(function (response) {
                if (response.ok) {
                    response.json()
                    .then(function (data) {
                        const chromatogram = JSON.parse(data.chromatogram)
                        return plotChromatogram(chromatogram, sampleName)
                    })
                }
                else {
                    console.log(
                        'fetch was not successfull:',
                        $(response.status)
                    );
                    return ;
                }
            })
        })
        
        // change mouse pointer to a hand when hovering over a row
        allRows[i].addEventListener('mouseover', function(e){
            this.style.cursor='pointer'
        })
    }
}
