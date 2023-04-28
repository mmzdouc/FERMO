import { createCytoGraph } from './cytoscape_graph.js';
import { selectRows } from './sampleTable.js';


//call functions
createCytoGraph(window.network, window.stylesheet)
selectRows()
