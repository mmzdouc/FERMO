#TO DO:
#-> for feature_object_creation(): use hash of int(ID) as key instead of
#only ind(ID) -> should prevent overwriting; however, there might be 
#hash-collisions that have the be caught before overwriting and entry

import pandas as pd
from .Feature_Object import Feature_Object
from .presence_in_samples import presence_in_samples
from .median_fwhm import median_fwhm

def feature_object_creation(peaktable: str, 
ms2spectra: dict) -> dict[int, "Feature_Object"]:
    """Scrape data from peaktable, create Feature Objects, store 
    in dict.
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    ms2spectra : `dict`
        Feature_ID(keys):[fragments,intensities](values)
    
    Returns
    -------
    features : `dict`
        Feature_ID(keys):Feature_Objects(values)
        
    Notes
    -------
    Core of feature object creation. Majority of data extraction.
    Feature creation.
    Iterates over pandas.dataframe and extracts data.
    TODO: 
    2) integrate: max:intensity, area
    """
    features = dict()
    for index, row in peaktable.iterrows():
        feature_ID = int(row["feature_ID"])
        precursor_mz = float(row["precursor_mz"])
        retention_time = float(row["retention_time"])
        presence_sample = presence_in_samples(row)
        fwhm = median_fwhm(row)
        tandem_mass_fragmentation = ms2spectra[feature_ID][0]
        tandem_mass_intensities = ms2spectra[feature_ID][1]
        ###creates objects###
        features[feature_ID] = Feature_Object(feature_ID, precursor_mz, 
        retention_time, presence_sample, fwhm, tandem_mass_fragmentation,
        tandem_mass_intensities)
    return features
