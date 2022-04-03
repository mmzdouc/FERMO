#TO DO:
#-> for feature_object_creation(): use hash of int(ID) as key instead of
#only ind(ID) -> should prevent overwriting; however, there might be 
#hash-collisions that have the be caught before overwriting and entry



import pandas as pd


class Feature_Object():
    """Initializes feature objects:
    
    Class to initialize feature (ft) objects.
    Data is extracted from a metabolomics peak table (here: MzMine2/3).
    
    'feature_ID' -> int-type ID of ft in the peak table.
    'precursor_mz' -> float-type mass-to-charge ratio of the ft.
    'retention_time' -> float-type retention time in mins of ft.
    'presence_sample' -> dict of sample name:intensity of ft across samples.
    'tandem_mass_fragmentation'* -> numpy-array of tandem mass fragments.
    'tandem_mass_intensities'* -> numpy-array of tandem mass frag intensities.
    
    Notes:
    -----
    *numpy-arrays for fragmentation and intensities correspond to each
    other. 
    Example: tandem_mass_fragmentation[0] -> tandem_mass_intensities[0]; etc. 
    -----
    """
    def __init__(self, feature_ID, precursor_mz, retention_time,
    presence_sample, tandem_mass_fragmentation, tandem_mass_intensities):
        self.feature_ID = feature_ID 
        self.precursor_mz = precursor_mz
        self.retention_time = retention_time
        self.presence_sample = presence_sample
        self.tandem_mass_fragmentation = tandem_mass_fragmentation
        self.tandem_mass_intensities = tandem_mass_intensities

def presence_in_samples(series):
    """Auxillary function:
    
    Extracts info about presence and intensity of peaks in samples
    from a python series; Specific for MzMine peak table.
    """
    samples = series[series!=0].filter(regex=".mzML|.mzXML")
    presence_sample = dict()
    for entry in samples.index:
        peak_intensity = samples.loc[entry]
        presence_sample[entry] = peak_intensity
    return presence_sample

def feature_object_creation(df, ms2dict):
    """Creates feature objects:
    
    Scrapes info for feature object initialization by iterating over
    MzMine3 style feature table.
    Returns dictionary of feature objects, w ID(key):feature object(value)
    """
    peak_storage = dict()
    for index, row in df.iterrows():
        feature_ID = int(row["row ID"])
        precursor_mz = float(row["row m/z"])
        retention_time = float(row["row retention time"])
        presence_sample = presence_in_samples(row)
        tandem_mass_fragmentation = ms2dict[feature_ID][0]
        tandem_mass_intensities = ms2dict[feature_ID][1]
        ###creates objects###
        peak_storage[feature_ID] = Feature_Object(feature_ID, precursor_mz, 
        retention_time, presence_sample, tandem_mass_fragmentation,
        tandem_mass_intensities)
    return peak_storage
