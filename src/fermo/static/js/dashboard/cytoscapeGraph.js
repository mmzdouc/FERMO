import { updateFeatureTable } from './featureTable.js';
import { plotMainChromatogram, plotCliqueChrom } from './chromatogram.js';

/**
 * Remove or create message for user when necessary and plot the cytoscape graph
 * 
 * @param {string} cytoMessage 
 */
export function updateCytoscape(cytoMessage){

    const cytoMessageP = document.querySelector('.text-danger')
    if (cytoMessageP) { // if a message already exists, remove it
        cytoMessageP.remove()
    }
    if (cytoMessage){ // if a message is given, display it to the user
        const cytoGraph = document.getElementById('cy')
        const parent = cytoGraph.parentNode // the element containing the cytoscape graph

        const cytoMessageP = document.createElement('p')
        cytoMessageP.classList.add('text-danger')
        cytoMessageP.textContent = cytoMessage
        parent.insertBefore(cytoMessageP, cytoGraph)
    }
    const cy = createCytoGraph(window.network, window.stylesheet)
    selectNode(cy)
}


/**
 * Create the cytoscape graph
 * 
 * @param {json} network - json object containing the nodes and edges of the graph
 * @param {json} stylesheet - json object containing the style of the graph
 */
function createCytoGraph(network, stylesheet) {
    return cytoscape({
        container: document.getElementById('cy'), // container to display graph
        elements: network, // list of graph elements
        style: stylesheet, // the stylesheet for the graph
        layout: {name: 'cose', rows: 1},
    })
}

/**
 * Add click event listener to nodes
 * 
 * @param {Object} cytoGraph the Cytoscape Object as give by cytoscape()
 */
function selectNode(cytoGraph) {
    cytoGraph.on('click', 'node', function(evt){
        window.featureID = evt.target.id()
        fetch(window.location.href, {
            method: 'POST',
            body: JSON.stringify({
                sample: [false, window.sampleName],
                featChanged: true,
                featID: window.featureID
            }),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(function (response) {
            if (response.ok) {
                response.json()
                .then(function (data){
                    if (Object.keys(data).length !== 0) { // if the response is not empty
                        // get the components of the response
                        const chromatogram = JSON.parse(data.chromatogram)
                        const featureTable = data.featTable
                        const cliqueChrom = JSON.parse(data.cliqueChrom)

                        // call respective functions
                        plotMainChromatogram(chromatogram)
                        plotCliqueChrom(cliqueChrom)
                        updateFeatureTable(featureTable)
                    }
                })
            }
            else {  // response was not ok
                console.log(
                    `fetch was not successfull: ${response.status}`
                )
                return ;
            }
        })
    })
}
