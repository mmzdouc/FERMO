
export function plotChromatogram(graph, sampleName){
    const chromHeading = document.getElementById('chromHeading')
    if (sampleName) {
        chromHeading.textContent = `Sample Chromatogram overview: ${sampleName}`
    }
    console.log('plotChromatogram() runs:')
    return Plotly.newPlot('mainChromatogram', graph, {});
}