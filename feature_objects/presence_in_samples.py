import pandas as pd


def presence_in_samples(row: str) -> dict[str, float]:
    """Extract presence of features in samples.
    
    Parameters
    ----------
    row : `pandas.core.series.Series`
        Row from MZmine3 peaktable
    
    Returns
    -------
    presence_sample : `dict`
        Sample names(keys):Intensities(values)
    
    Notes
    -------
    Extracts info about presence and intensity of peaks in samples
    from a python series.
    Can process different input tables, based on if the sample 
    columns contain "Peak area" (peaktable SIMPLE) or if the rows
    contain "DETECTED" (peaktable ALL)
    """
    #switch for different input tables: SIMPLE or ALL 
    #MZmine3 table SIMPLE
    if not row.filter(regex="Peak").empty:
        #extract sample names in which feature was detected
        feature_in_samples = []
        for lable in row[row!=0].filter(regex=".mzML|.mzXML").index:
            feature_in_samples.append(lable.split(" ")[0])
        #build dict
        presence_sample = dict()
        for element in feature_in_samples:
            query = "".join([element, " Peak area"])
            peak_intensity = row[query]
            presence_sample[element] = float(peak_intensity)
        return presence_sample
    #MZmine3 table ALL
    else:
        #extract sample names in which feature was detected
        feature_in_samples = []
        for lable in row[row=="DETECTED"].index:
            feature_in_samples.append(lable.split(":")[1])
        #build dict
        presence_sample = dict()
        for element in feature_in_samples:
            query = "".join(["datafile:", element, ":intensity_range:max"])
            peak_intensity = row[query]
            presence_sample[element] = float(peak_intensity)
        return presence_sample
