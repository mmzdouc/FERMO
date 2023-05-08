import { updateCytoscape } from './cytoscapeGraph.js';
import { updateFeatureTable } from './featureTable.js';

/**
 * Plot the chromatogram of the selected sample
 *
 * @param {JSON} chromatogram - JSON object containing the data for the chromatogram
 * @param {string} sampleName - selected sample
 */
export function plotChromatogram(chromatogram, sampleName=''){
    const chromHeading = document.getElementById('chromHeading')
    if (sampleName) {
        chromHeading.textContent = `Sample Chromatogram overview: ${sampleName}`
    }
    const chromID = 'mainChromatogram'
    Plotly.newPlot(chromID, chromatogram, {})
    selectFeatures(chromID)
    return
}


/**
 * Make features in the chromatogram selectable and handle the event
 * -> update the chromatogram itself, the feature table and the cytoscape graph
 * 
 * @param {string} chromID - id of the div containing the chromatogram
 */
export function selectFeatures(chromID){
    const chromatogramDiv = document.getElementById(chromID)
    chromatogramDiv.on('plotly_click', function(data){
        window.featureIndex = data.points[0].curveNumber
        fetch(window.location.href, {
            method: 'POST',
            body: JSON.stringify({
                sample: [false, window.sampleName],  // set first element to false to indicate that the sample did not change
                featIndex: [true, window.featureIndex]  // set first element to true to indicate that a feature was selected
            }),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(function (response) {
            if (response.ok) {
                response.json()
                .then(function (data) {
                    // get the components of the response
                    const chromatogram = JSON.parse(data.chromatogram)
                    const featureTable = JSON.parse(data.featTable)
                    window.network = JSON.parse(data.network)
                    const cytoMessage = JSON.parse(data.cytoscapeMessage)
                    
                    // call respective functions
                    plotChromatogram(chromatogram)
                    updateFeatureTable(featureTable)
                    updateCytoscape(cytoMessage)
                })
            }
            else {
                console.log(
                    `fetch was not successfull: ${response.status}`
                )
                return ;
            }
        })
    })
}
