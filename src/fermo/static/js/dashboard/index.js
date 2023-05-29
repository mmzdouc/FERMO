import { sampleOverviewTable, updateTable } from './featureTable.js';
import { plotMainChromatogram } from './chromatogram.js';
import { selectRows } from './sampleTable.js';
import { filterFeatures } from './filterPanel.js';


//call functions
updateTable(window.general_sample_table, '#generalSampleTable tbody')
sampleOverviewTable(window.specific_sample_table, '#sampleOverviewTable tbody')
plotMainChromatogram(window.graph)
selectRows()
filterFeatures()
