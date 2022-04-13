#TO DO:
#-> for feature_object_creation(): use hash of int(ID) as key instead of
#only ind(ID) -> should prevent overwriting; however, there might be 
#hash-collisions that have the be caught before overwriting and entry

import pandas as pd
from .Feature_Object import Feature_Object
from .presence_in_samples import presence_in_samples
from .find_median_fwhm import find_median_fwhm
from .find_max_intensity import find_max_intensity

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
    """
    features = dict()
    for index, row in peaktable.iterrows():
        feature_ID = int(row["feature_ID"])
        precursor_mz = float(row["precursor_mz"])
        retention_time = float(row["retention_time"])
        sample_names_intensities = presence_in_samples(row)
        presence_samples = sample_names_intensities[0]
        intensities_samples = sample_names_intensities[1]
        median_fwhm = find_median_fwhm(row)
        feature_max_int = find_max_intensity(row)
        tandem_mass_fragmentation = ms2spectra[feature_ID][0]
        tandem_mass_intensities = ms2spectra[feature_ID][1]
        ###creates objects###
        features[feature_ID] = Feature_Object(feature_ID, precursor_mz, 
        retention_time, presence_samples, intensities_samples, 
        median_fwhm, feature_max_int, tandem_mass_fragmentation,
        tandem_mass_intensities)
    return features
