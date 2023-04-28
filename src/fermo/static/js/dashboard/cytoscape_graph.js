/**
 * 
 * @param {json} network - json object containing the nodes and edges of the graph
 * @param {json} stylesheet - json object containing the style of the graph
 */
export function createCytoGraph(network, stylesheet) {
    return cytoscape({
        container: document.getElementById('cy'), // container to display graph
        elements: network, // list of graph elements
        style: stylesheet, // the stylesheet for the graph
        layout: {name: 'cose', rows: 1},
    });
}