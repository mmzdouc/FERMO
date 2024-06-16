/* Data extraction functions to be used in the dashboard

Copyright (c) 2024-present Hannah Esther Augustijn, MSc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

export function getSampleData(sampleName, statsChromatogram) {
    // Extract sample data for plotting chromatogram lines
    var activeSampleData = statsChromatogram[sampleName];

    // Get the max and min RT across all samples to use as plot range
    const allTraceRtValues = Object.values(statsChromatogram).
    flatMap(sample => sample.flatMap(obj => obj.trace_rt));
    const maxRt = Math.max(...allTraceRtValues);
    const minRt = Math.min(...allTraceRtValues);

    return {
        traceInt: activeSampleData.map(obj => obj.trace_int),
        traceRt: activeSampleData.map(obj => obj.trace_rt),
        featureId: activeSampleData.map(obj => obj.f_id),
        absInt: activeSampleData.map(obj => obj.abs_int),
        relInt: activeSampleData.map(obj => obj.rel_int),
        retTime: activeSampleData.map(obj => obj.rt),
        precMz: activeSampleData.map(obj => obj.mz),
        novScore: activeSampleData.map(obj => obj.novelty),
        blankAs: activeSampleData.map(obj => obj.blank),
        fNetworkCosine: activeSampleData.map(obj => obj.n_features_cosine),
        fNetworkDeepScore: activeSampleData.map(obj => obj.n_features_deepscore),
        idNetCos: activeSampleData.map(obj => obj.n_cos_id),
        idNetMs: activeSampleData.map(obj => obj.n_ms2d_id),
        samples: activeSampleData.map(obj => obj.samples),
        fGroupData: activeSampleData.map(obj => obj.f_group),
        fSampleData: activeSampleData.map(obj => obj.f_sample),
        aSampleData: activeSampleData.map(obj => obj.a_sample),
        annotations: activeSampleData.map(obj => obj.annotations),
        retTimeAvg: activeSampleData.map(obj => obj.rt_avg),
        upLowRange: [minRt - minRt * 0.05, maxRt + maxRt * 0.02]
    }
}

export function getFeatureData(featureId, sampleData, networkType) {
    let filteredData = {
        featureId: [],
        fNetwork: [],
        traceInt: [],
        traceRt: [],
        precMz: [],
        retTime: [],
        relInt: [],
        absInt: [],
        upLowRange: [],
        blankAs: [],
        novScore: [],
        target: []
    };

    // Iterate through the original sampleData to find matching features
    for (var i = 0; i < sampleData.featureId.length; i++) {
        if (sampleData.featureId[i] == featureId) {
            filteredData.upLowRange.push(sampleData.upLowRange[0], sampleData.upLowRange[1]);
            let networkType2;
            if (networkType === "modified_cosine") {
                networkType2 = "fNetworkCosine";
            } else if (networkType === "ms2deepscore") {
                networkType2 = "fNetworkDeepScore";
            }
            filteredData.fNetwork.push(sampleData[networkType2][i]);

            // Iterate through the fNetwork array to find the corresponding features
            for (var j = 0; j < sampleData[networkType2][i].length; j++) {
                let key = sampleData[networkType2][i][j];
                let index = sampleData.featureId.indexOf(key);

                if (index >= 0 && index < sampleData.traceInt.length) {
                    filteredData.target.push(sampleData.featureId[index] == featureId ? 'selected' : 'related');
                    filteredData.featureId.push(sampleData.featureId[index]);
                    filteredData.traceInt.push(sampleData.traceInt[index]);
                    filteredData.traceRt.push(sampleData.traceRt[index]);
                    filteredData.blankAs.push(sampleData.blankAs[index]);
                    filteredData.precMz.push(sampleData.precMz[index]);
                    filteredData.precMz.push(sampleData.novScore[index]);
                    filteredData.retTime.push(sampleData.retTime[index]);
                    filteredData.absInt.push(sampleData.absInt[index]);
                    filteredData.relInt.push(sampleData.relInt[index]);
                }
            }
        }
    }
    return filteredData;
}

export function getUniqueFeatureIds(sampleData) {
    const fIdCounts = {};

    for (const sampleName in sampleData) {
        if (sampleData.hasOwnProperty(sampleName)) {
            const sampleFeatures = sampleData[sampleName];
            sampleFeatures.forEach(feature => {
                const fId = feature.f_id;
                if (fIdCounts[fId]) {
                    fIdCounts[fId]++;
                } else {
                    fIdCounts[fId] = 1;
                }
            });
        }
    }

    const uniqueFIds = [];
    for (const fId in fIdCounts) {
        if (fIdCounts[fId] === 1) {
            uniqueFIds.push(fId);
        }
    }

    return uniqueFIds;
}

export function getFeatureDetails(uniqueNIds, sampleData) {
    const result = [];
    const seenIds = new Set();

    const uniqueNIdsStr = uniqueNIds.map(id => id.toString());

    for (const sampleName in sampleData) {
        if (sampleData.hasOwnProperty(sampleName)) {
            const features = sampleData[sampleName];
            for (const feature of features) {
                const featureIdStr = feature.f_id.toString();
                if (uniqueNIdsStr.includes(featureIdStr) && !seenIds.has(featureIdStr)) {
                    result.push(feature);
                    seenIds.add(featureIdStr);
                }
            }
        }
    }

    return result;
}
