
import { plotChromatogram } from './chromatogram.js';
import { createCytoGraph } from './cytoscape_graph.js';
import { selectRows } from './sampleTable.js';


//call functions
plotChromatogram(window.graph)
createCytoGraph(window.network, window.stylesheet)
selectRows()
