import pandas as pd

def filter_for_topn_features(samples: str, topn: float
) -> dict:
    """Filters features after their relative intensity.
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    topn : `float`
        Float between 0 and 1. Is the quantile of features that is 
        retained. E.g. 0.9 means: 90th quantile -> remove features 
        that have a relative intensity of less than 0.1 of feature 
        with highest intensity (1.0).
    
    Returns
    -------
    returned_samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    """
    returned_samples  = dict()
    assert topn > 0, f"""
WARNING: a value of {topn} was given for topn.
This discards all features. Consider a more sensible value
(e.g. 0.95 or 0.99 to remove the bottom 5% or 1% of features)
and try again."""
    topn = 1 - topn
    for sample in samples:
        #filter for samples that have an relative intensity of 
        #greater than or equal to 1-topn (e.g. 0.05)
        sample_filtered = samples[sample].loc[
        samples[sample].loc[:,"min_max_norm_intensity"] >= topn]
        #reset index
        sample_filtered.reset_index(drop=True, inplace=True)
        returned_samples[sample] = sample_filtered
    return returned_samples
