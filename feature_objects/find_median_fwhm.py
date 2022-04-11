import pandas as pd


def find_median_fwhm(row: str) -> float:
    '''Extract feature width at half maximum intensity and calc median.
    
    Parameters
    ----------
    row : `pandas.core.series.Series`
        Row from MZmine3 peaktable
    
    Returns
    -------
    fwhm : `float`
        median feature width at half maximum intensity in minutes.
    
    Notes
    -------
    Covers two kind of MzMine3 tables (ALL and SIMPLE); in case 
    of SIMPLE, the fwhm is missing, so a fake one (0.2 min) is provided.
    '''
    filter_for_fwhm = row.filter(regex=":fwhm$").dropna()
    #peaktable ALL
    if not filter_for_fwhm.empty:
        fwhm = float(filter_for_fwhm.median())
        return fwhm
    #peaktable SIMPLE
    else:
        fwhm = 0.2
        return fwhm
