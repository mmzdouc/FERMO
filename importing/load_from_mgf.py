from pyteomics import mgf

#####

def load_from_mgf(arg):
    '''Load spectrum(s) from mgf file.
    
    This function reads spectra from a mgf file and returns a dict
    where the spectrum IDs are the keys and a list of the fragment
    and intensity numpy arrays are the values. 
    '''
    ID_to_msms = dict()
    for spectrum in mgf.read(open(arg)):
        fragments = spectrum.get('m/z array')
        intensities = spectrum.get('intensity array')
        ID = int(spectrum.get('params').get('feature_id'))
        ID_to_msms[ID] = [fragments, intensities]
    return ID_to_msms

