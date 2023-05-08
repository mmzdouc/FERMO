
import { plotChromatogram } from './chromatogram.js';
import { createCytoGraph } from './cytoscapeGraph.js';
import { selectRows } from './sampleTable.js';


//call functions
plotChromatogram(window.graph)
createCytoGraph(window.network, window.stylesheet)
selectRows()
