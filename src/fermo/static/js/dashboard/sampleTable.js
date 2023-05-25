import { plotMainChromatogram, plotCliqueChrom } from './chromatogram.js';
import { updateCytoscape } from './cytoscapeGraph.js';
import { updateTable } from './featureTable.js';

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
            window.sampleName = this.getAttribute('data-value')
            // send POST request to current URL
            fetch(window.location.href, {
                method: 'POST',
                body: JSON.stringify({
                    sample: [true, window.sampleName],  // set first element to true to indicate that a sample was selected
                    featChanged: false,
                    featIndex: window.featureIndex
                }),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
            // define what to do with the response
            .then(function (response) {
                if (response.ok) {
                    response.json()
                    .then(function (data) {
                        // get the components of the response
                        const chromatogram = JSON.parse(data.chromatogram)
                        const cliqueChrom = JSON.parse(data.cliqueChrom)
                        const featureTable = data.featTable
                        window.network = data.network
                        const cytoMessage = JSON.parse(data.cytoscapeMessage)
                        // const nodedata - JSON.parse(data.nodedata) but nodedata should prob be given to the network so that cytoscape can display hover information

                        plotMainChromatogram(chromatogram, sampleName)
                        plotCliqueChrom(cliqueChrom)
                        updateTable(featureTable, '#featureTable tbody')
                        updateCytoscape(cytoMessage)
                    })
                }
                else {
                    console.log(
                        `fetch was not successfull: ${response.status}`
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
