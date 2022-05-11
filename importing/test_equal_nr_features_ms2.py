import pandas as pd
import sys


def test_equal_nr_features_ms2(
peaktable: str, ms2spectra_dict: str):
    """Display sample scores and topn of features
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    ms2spectra_dict : `dict`

    Notes
    -----
    Checks if each row (feature_ID) is in ms2spectra_dict; if not,
    raises error and exits
    """
    
    #pull out nr of features from peaktable
    for i in peaktable.loc[:,"feature_ID"].to_list():
        if not i in ms2spectra_dict:
            sys.exit(
f"""FATAL ERROR: ABORT
    FeatureID {i} is missing an accompanying ms/ms spectrum.
    To make FERMO run properly, ms/ms spectra are needed for each 
    feature. Please change your MzMine settings so that features 
    without a ms/ms spectrum are filtered from the peaktable and
    try again.""")
        else:
            continue
