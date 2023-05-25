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
    addHoverEvent(cy)
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
                        try {
                            window.network = JSON.parse(data.network)
                        } catch (SyntaxError) {
                            window.network = []
                        }
                        const cytoMessage = JSON.parse(data.cytoscapeMessage)

                        // call respective functions
                        plotMainChromatogram(chromatogram)
                        plotCliqueChrom(cliqueChrom)
                        updateFeatureTable(featureTable)
                        updateCytoscape(cytoMessage)

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


/**
 * Add hover event listener to nodes and edges
 * 
 * @param {Object} cytoGraph
 */
function addHoverEvent(cytoGraph){
    cytoGraph.on('mouseover', 'node', function(evt){
        const nodeData = evt.target['_private'].data
        fetch(window.location.href, {
            method: 'POST',
            body: JSON.stringify({
                sample: [false, window.sampleName],
                featChanged: false,
                nodeData: nodeData,
            }),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(handleResponse)
    })
    cytoGraph.on('mouseover', 'edge', function(evt){
        const edgeData = evt.target['_private'].data
        fetch(window.location.href, {
            method: 'POST',
            body: JSON.stringify({
                sample: [false, window.sampleName],
                featChanged: false,
                edgeData: edgeData,
            }),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(handleResponse)
    })
    cytoGraph.on('mouseout', 'node', mouseoutEvent)
    cytoGraph.on('mouseout', 'edge', mouseoutEvent)
}


function handleResponse(response){
    if (response.ok) {
        response.json()
        .then(function (data){
            createPopover(data)
        })
    } else {
        console.log(
            `fetch was not successfull: ${response.status}`
        )
        return ;
    }
}

/**
 * Remove popovers after a delay when mouse leaves node or edge
 * @param {Object} evt 
 */
async function mouseoutEvent(evt){
    const delay = ms => new Promise(res => setTimeout(res, ms))  // utility function to wait 
    await delay(100)  // wait to let mouseover-event finish first
    const popovers = document.querySelectorAll('.popover')
    for (let popover of popovers) {
        popover.remove()
    }
}

/**
 * Create a popover for the element that is hovered over
 *
 * @param {Array} data
*/
function createPopover(data){
    const header = data.shift() // access and remove first element of array
    const cytoDiv = document.getElementById('cy')

    const popover = document.createElement('div')
    popover.classList.add('card', 'popover')

    const popoverHeader = document.createElement('div')
    popoverHeader.classList.add('card-header', 'popoverHeader')
    popoverHeader.innerHTML= header

    const popoverBody = document.createElement('div')
    popoverBody.classList.add('card-body')

    const bulletList = document.createElement('ul')
    for (let row of data){
        let bulletPoint = document.createElement('li')
        bulletPoint.innerHTML = `${row[0]}: ${row[1]}`
        bulletList.append(bulletPoint)
    }
    popoverBody.append(bulletList)

    popover.append(popoverHeader, popoverBody)
    cytoDiv.append(popover)

    return popover
}
