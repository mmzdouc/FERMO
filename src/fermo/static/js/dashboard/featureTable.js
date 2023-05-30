import { bulletList } from './cytoscapeGraph.js'

/**
 * Update the table: remove the old table and loop over the content of
 * the new table to create the new one with correct formatting.
 *
 * @param {string|object} featureTable the string containing the actual content
 * @param {string} selector css selector for the table body
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


/**
 * Create/update sampleOverview Table with tooltips and data-values
 * 
 * @param {Array} content
 */
export function sampleOverviewTable(content){
    let tableHead = document.querySelector('#sampleOverviewTable thead')
    let tableBody = document.querySelector('#sampleOverviewTable tbody')
    // "empty" the table
    tableHead.replaceChildren()
    tableBody.replaceChildren()
    
    // create tablehead
    tableHead.setAttribute('class', 'align-middle')
    const headrow = document.createElement('tr')
    const cols = ['Filename', 'Group', 'Selected features', 'Selected networks']
    for (let i=0; i<cols.length; i++){
        let th = document.createElement('th')
        th.setAttribute('scope', 'col')
        th.classList.add('py-1')
        th.innerHTML = cols[i]
        headrow.append(th)
    }
    tableHead.append(headrow)

    // create tablebody
    const sampleInfoDescriptors = [
        'Filename',
        'Diversity-score',
        'Spec score',
        'Mean novelty score',
        'Total',
        'Non-blank',
        'Blank & MS1'
    ]
    for (let i=0; i<content.length; i++){
        let row = content[i]
        // assemble content for the 'tooltip'
        let sampleInfoData = row.slice(4)
        sampleInfoData.unshift(row[0])
        let zipped = sampleInfoDescriptors.map((x, i) => [x, sampleInfoData[i]])
        let sampleInfoContent = bulletList(zipped).outerHTML
        let rowElem = document.createElement('tr')

        rowElem.setAttribute('data-value', row[0])
        // set attributes for the 'tooltip' to work
        rowElem.setAttribute('data-bs-toggle', 'tooltip')
        rowElem.setAttribute('data-bs-html', 'true')
        rowElem.setAttribute('data-bs-title', sampleInfoContent)
        rowElem.setAttribute('data-bs-placement', 'right')
        rowElem.setAttribute('data-bs-custom-class', 'custom-tooltip')

        // fill table cells with content
        for (let j=0; j<4; j++){
            let dataElem = document.createElement('td')
            dataElem.classList.add('p-1')
            dataElem.innerHTML = row[j]
            rowElem.append(dataElem)
        }
        tableBody.append(rowElem)
    }
    // initiate the new tooltips
    initiateTooltips()
}


/**
 * Create sampleStatsTable
 * 
 * @param {Array} content
 */
export function sampleStatsTable(content){
    const tableHead = document.querySelector('#generalSampleTable thead')
    const tableBody = document.querySelector('#generalSampleTable tbody')

    tableHead.replaceChildren()
    tableBody.replaceChildren()

    // create tablehead
    tableHead.classList.add('lh-sm')
    const headRow = document.createElement('tr')
    const cols = ['Number of', 'Value']
    for (let i=0; i<cols.length; i++){
        let headCell = document.createElement('th')
        headCell.setAttribute('scope', 'col')
        headCell.classList.add('col', 'col-7')
        headCell.append(cols[i])
        headRow.append(headCell)
    }
    tableHead.append(headRow)

    // create tablebody
    const attributes = [
        "Total samples:",
        "Total features:",
        "Selected features:",
        "Selected networks:",
        "Non-blank:",
        "Blank & MS1:"
    ]
    let zipped = attributes.map((x, i) => [x, content[i]])
    for (let row of zipped) {
        let rowElem = document.createElement('tr')
        for (let cell of row){
            let dataElem = document.createElement('td')
            dataElem.classList.add('p-1')
            dataElem.innerHTML = cell
            rowElem.append(dataElem)
        }
        tableBody.append(rowElem)
    }
}
