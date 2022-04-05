def precursor_search(feature_objects, precursor_mz):
    """Search-function:
    
    Looks for precursor_mz (float or integer) in dict feature objects. 
    To match more flexibely, the output is:
    precursor_mz >= output < (precursor_mz + 1)
    
    Example:
    -----
    precursor_search(feature_objects, 522):
    returns; 522.1, 522.2, ... 522.9
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

            
