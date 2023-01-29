def set_from_sample_tables(
    samples,
    ):
    """Return set from features in all sample dataframes
    
    Parameters
    ----------
    samples : `dict`
    
    Returns
    -------
    detected_features : `set`
    """
    detected_features = set()
    for sample in samples:
        detected_features.update(set(samples[sample]['feature_ID']))
    return detected_features
