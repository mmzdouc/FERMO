
/**
 * Remove or create message for user when necessary and update the cytoscape graph
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
    createCytoGraph(window.network, window.stylesheet)
}


/**
 * Create the cytoscape graph
 * @param {json} network - json object containing the nodes and edges of the graph
 * @param {json} stylesheet - json object containing the style of the graph
 */
export function createCytoGraph(network, stylesheet) {
    return cytoscape({
        container: document.getElementById('cy'), // container to display graph
        elements: network, // list of graph elements
        style: stylesheet, // the stylesheet for the graph
        layout: {name: 'cose', rows: 1},
    })
}