
/**
 * Update the feature table: remove the old table and loop over the content of
 * the new featureTable to create the new one with correct formatting.
 * @param {string} featureTable 
 */
export function updateFeatureTable(featureTable){
    let featureArray = []
    if (typeof(featureTable) == 'string'){
        featureArray = tableStringToArray(featureTable)
    } else {
        featureArray = featureTable
    }
    let tableBody = document.querySelector('#featureTable tbody')
    // remove old table
    tableBody.replaceChildren()
    // create new table
    for (let row of featureArray){
        let rowElem = document.createElement('tr')
        for (let cell of row){
            let dataElem = document.createElement('td')
            if (cell == '-----'){
                dataElem.classList.add('p-0')
                dataElem.innerHTML = '<hr>'
            } else {
                dataElem.classList.add('p-1')
                dataElem.innerHTML = cell
            }
            rowElem.append(dataElem)
        }
        tableBody.append(rowElem)
    }
}


/**
 * Convert the featureTable-string into a nested array
 * 
 * @param {string} featureTable - string that represents a list of lists from python
 * 
 * @returns {Array}
 */
function tableStringToArray(featureTable){
    // remove first and last two characters of the 'string'
    featureTable = featureTable.slice(2, -2)
    // split to separate the 'rows'
    let featureArr = featureTable.split('], [')
    let featureArray = []
    for (let row of featureArr){
        // split to separate the 'cells'
        row = row.split(', ')
        for (let i=0; i<row.length; i++){
            if (row[i].startsWith('"')){
                // remove quotes
                row[i] = row[i].slice(1, -1)
                // remove newline characters if present
                if (row[i].includes('blank')){
                    row[i] = row[i].slice(0, 61) + row[i].slice(63)
                }
            }
        }
        featureArray.push(row)
    }
    return featureArray
}