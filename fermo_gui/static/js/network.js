
export function visualizeNetwork(fId, statsNetwork, filteredSampleData, cos_id, ms2_id) {
    console.log(statsNetwork.modified_cosine[cos_id])

    var filteredFeatureIds = filteredSampleData.featureId.filter(id => id.toString() !== fId);

    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: statsNetwork.modified_cosine[cos_id].elements,

        layout: {
            name: 'cose',
            rows: 1
        },

        style: [
            {
                selector: 'node',
                style: {
                    "background-color": "#b2b6b9",
                    color: "white",
                    "border-color": "white",
                    "border-width": 4
                }
            },
            {
                selector: 'edge',
                style: {
                    "curve-style": "bezier",
                    "width": "mapData(weight, 0.5, 1, 1, 10)"
                }
            },
            {
                selector: 'node[id = "' + fId + '"]',
                style: {
                    "background-color": "#f4aaa7",
                    "border-color": "#960303",
                    "border-width": 4
                }
            },
            {
                selector: filteredFeatureIds.map(id => 'node[id = "' + id + '"]').join(', '),
                style: {
                    "background-color": "#c6dcfb",
                    "border-color": "#227aa0",
                    "border-width": 4
                }
            },
            {
                selector: 'node:selected',
                style: {
                  'background-color': '#83a688',
                  'border-color': '#485c4b',
                }
            },
            {
                selector: 'edge:selected',
                style: {
                    'line-color': '#F08080',
                    "target-arrow-color": "#F08080",
                }
            },
        ],

    });

}