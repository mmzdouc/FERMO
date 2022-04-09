from pyteomics import mgf

#####

def load_from_mgf(arg: str) -> dict[int, list[int, int]]:
    '''Load spectrum(s) from mgf file using module pyteomics.
    
    Parameters
    ----------
    arg : `str`
        Reads a .mgf-file in MzMine3-format (GNPS Export Module/Submit
        Module)

    Returns
    -------
    ms2spectra : `dict`
        For each spectrum in the .mgf-file, a one-dimensional numpy
        array for the ms2 fragments and the fragment
        intensities is created. The arrays are stored in a list. The
        list is the value, the key is the feature ID
    '''
    ms2spectra = dict()
    for spectrum in mgf.read(open(arg)):
        fragments = spectrum.get('m/z array')
        intensities = spectrum.get('intensity array')
        feature_ID = int(spectrum.get('params').get('feature_id'))
        ms2spectra[feature_ID] = [fragments, intensities]
    return ms2spectra

