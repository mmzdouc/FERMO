import matchms


class Feature_Object():
    """Initialize feature objects from MZmine3 peaktable:
    
    Parameters
    ----------
    feature_ID : `int`
        ID of feature.
    precursor_mz : `float`
        mz (mass-to-charge-ratio) of feature.
    retention_time : `float`
        retention time (in mins) of feature.
    presence_sample : `dict` #can maybe be cut, not so interesting
        sample name:intensity of features across samples.
    median_fwhm : `float`
        median feature width at half maximum across samples
    feature_max_int: `float`
        maximum intensity/peak height of feature across samples
    ms2spectrum : `matchms.Spectrum`
        contains fragments, intensities, and precuresor_mz utilizing
        matchms.Spectrum structure (object in an object)
        
    Examples
    -------
    Define a minimal feature object:
    
    >>> import matchms, numpy
    >>> Feature_Object(1, 100.0, 1.0, {"ex.mzXML" : 200.0}, 0.2,
    200.0, numpy.array([100.1, 150.1]), numpy.array([20.0, 80.0]))
    """
    def __init__(self, feature_ID, precursor_mz, retention_time,
    presence_sample, median_fwhm, feature_max_int, 
    tandem_mass_fragmentation, tandem_mass_intensities):
        self.feature_ID = feature_ID 
        self.precursor_mz = precursor_mz
        self.retention_time = retention_time
        self.presence_sample = presence_sample
        self.median_fwhm = median_fwhm
        self.feature_max_int = feature_max_int
        self.ms2spectrum = matchms.Spectrum(tandem_mass_fragmentation,
        tandem_mass_intensities, {"precursor_mz": precursor_mz})
