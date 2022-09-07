def assert_peaktable_format(peaktable):
    """Test peaktable columns for correct headers (i.e. format)
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`

    Notes
    -----
    Assert has to evaluate to True to pass; if false, AssertionError
    is raised and script is terminated
    """
    
    assert not peaktable.filter(regex="^id$").columns.empty
    assert not peaktable.filter(regex="^mz$").columns.empty
    assert not peaktable.filter(regex="^rt$").columns.empty
    assert not peaktable.filter(regex="^datafile:").columns.empty
    assert not peaktable.filter(regex=":intensity_range:max$").columns.empty
    assert not peaktable.filter(regex=":feature_state$").columns.empty
    assert not peaktable.filter(regex=":fwhm$").columns.empty
    assert not peaktable.filter(regex=":rt$").columns.empty
    assert not peaktable.filter(regex=":rt_range:min$").columns.empty
    assert not peaktable.filter(regex=":rt_range:max$").columns.empty

