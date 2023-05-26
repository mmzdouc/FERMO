
/**
 * Update the table: remove the old table and loop over the content of
 * the new table to create the new one with correct formatting.
 *
 * @param {string|object} featureTable
 * @param {string} selector - css selector for the table body
 * 
 * @notes
 * Variables are only called featureSomething because the function was 
 * originally only intended for the feature table.
 * 
 * Relies on the template to already have a table body. If the macros in
 * dashboard.html are removed, it must be modified to create a table body from
 * scratch
 */
export function updateTable(featureTable, selector){
    let featureArray = []
    if (typeof(featureTable) == 'string'){
        featureArray = tableStringToArray(featureTable)
    } else {
        featureArray = featureTable
    }
    let tableBody = document.querySelector(selector)
    // remove old table
    tableBody.replaceChildren()
    // create new table but check if it contains objects or numbers
    if (typeof(featureArray[0]) == 'object'){
        for (let row of featureArray){
            let rowElem = document.createElement('tr')
            rowElem.setAttribute('data-value', row[0])
            for (let cell of row){
                let dataElem = document.createElement('td')
                if (cell == '-----'){
                    dataElem.classList.add('p-0')
                    dataElem.innerHTML = '<hr>'
                } else if (selector == '#sampleOverviewTable tbody' && typeof(cell) == 'string' && cell.length > 20){
                    console.log('in featureTable.js: string was long')
                    cell = cell.slice(0, 16) + '...'
                    dataElem.classList.add('p-1')
                    dataElem.innerHTML = cell
                } else {
                    dataElem.classList.add('p-1')
                    dataElem.innerHTML = cell
                }
                rowElem.append(dataElem)
            }
            tableBody.append(rowElem)
        }
    }
    else { // featureArray contains numbers like in sample stats table
        let rowElem = document.createElement('tr')
        for (let cell of featureArray){
            let dataElem = document.createElement('td')
            dataElem.classList.add('p-1')
            dataElem.innerHTML = cell
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
    // remove outer brackets
    featureTable = featureTable.slice(2, -2)
    // split to separate the 'rows'
    let featureArr = featureTable.split('], [')
    let featureArray = []
    for (let row of featureArr){
        /* split to separate the 'cells' (string.split() does not work because
           there is no unambiguous separator) */
        row = [row.substring(0, row.indexOf(", ")), row.substring(row.indexOf(", ")+2)]
        for (let i=0; i<row.length; i++){
            if (row[i].startsWith('"') || row[i].startsWith("'")){
                // remove quotes
                row[i] = row[i].slice(1, -1)
                /* remove newline characters if present; 'blank' is an 
                   indicator because it occurs in those lines where the
                   html-'a'-tag was used */
                if (row[i].includes('blank')){
                    row[i] = row[i].slice(0, 61) + row[i].slice(63)
                }
            }
        }
        featureArray.push(row)
    }
    return featureArray
}