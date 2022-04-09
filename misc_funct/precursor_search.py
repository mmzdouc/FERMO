def precursor_search(feature_objects: dict, precursor_mz: int):
    """Search and find feature object with certain precursor mz.
    
    Parameters
    ----------
    feature_objects : `dict`
        Contains Feature_Object objects
    precursor_mz: `int``
        precursor mz to search for
    
    Example:
    -----
    >>>precursor_search(feature_objects, 522):
    returns; 522.1, 522.2, ... 522.9
    
    Notes
    -------
    Proof of concept; will be adapted in the future
    """
    for entry in feature_objects:
        if (feature_objects[entry].precursor_mz >= precursor_mz) \
        & (feature_objects[entry].precursor_mz < (precursor_mz + 1.0)):
            #####Start return message
            print(feature_objects[entry].precursor_mz, 
            "(m/z) with the retention time ", 
            feature_objects[entry].retention_time, 
            "(min) has the ID", feature_objects[entry].feature_ID)
            #####Stop return message
