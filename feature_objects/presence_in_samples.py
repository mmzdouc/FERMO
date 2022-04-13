import pandas as pd
import numpy as np


def presence_in_samples(row: str) -> list[np.array, np.array]:
    """Extract presence of features in samples.
    
    Parameters
    ----------
    row : `pandas.core.series.Series`
        Row from MZmine3 peaktable
    
    Returns
    -------
    samples_intensities : `list`
        numpy array of sample names, numpy array of intensities
    
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
        presence_sample = []
        for label in row[row!=0].filter(regex=".mzML|.mzXML").index:
            presence_sample.append(label.split(" ")[0])
        #extract intensity of feature in sample
        intensity_in_sample = []
        for element in presence_sample:
            query = "".join([element, " Peak area"])
            intensity_in_sample.append(float(row[query]))
        #build list of numpy arrays
        samples_intensities = [np.array(presence_sample, dtype=object), 
        np.array(intensity_in_sample)]
        return samples_intensities
    #MZmine3 table ALL
    elif not row.filter(regex="^datafile:").empty:
        #extract sample names in which feature was detected
        presence_sample = []
        for label in row[row=="DETECTED"].index:
            presence_sample.append(label.split(":")[1])
        #extract intensity of feature in sample
        intensity_in_sample = []
        for element in presence_sample:
            query = "".join(["datafile:", element, ":intensity_range:max"])
            intensity_in_sample.append(float(row[query]))
        #build list of numpy arrays
        samples_intensities = [np.array(presence_sample, dtype=object), 
        np.array(intensity_in_sample)]
        return samples_intensities
    else:
        print("WARNING: presense of features in samples was no detemined.")
        print("WARNING: Only MzMine3-style peaktables are supported")
        raise ValueError

