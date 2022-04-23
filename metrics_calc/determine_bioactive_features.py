import pandas as pd

def determine_bioactive_features(
bioactivity_samples: dict,
samples: dict,
feature_objects: dict,
bioact_factor: int) -> list:
    """Separate bioactive features from 
    
    Parameters
    ----------
    bioactivity_samples : `dict`
        contains two lists (active, inactive) of samples generated
        by function importing.read_from_bioactiv_table
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    bioact_factor : `int`
        factor to determine if a feature, detected in both an active
        and an inactive sample, can be considered to be bioactivity
        associated
    
    Returns
    -------
    list_bioactivity_associated : `list`
        list of bioactivity-associated features
    
    Notes
    -----
    Compares set of features from bioactive samples against set
    of features from inactive samples (non-redundant).
    For features from active samples, keep the lowest intensity.
    for features from inactive samples, keep the highest intensity.
    If a feature is found only in active samples, count it as an 
    activity-associated feature.
    If a feature is found in both an active and an inactive sample,
    compare their intensities: the minimum intensity detected
    for activity, and the maximum intensity detected for inactivity. 
    If the minimum active intensity is n times higher (e.g. 10)
    than the maximum inactive intensity, count as an activity-associated
    feature. Else, consider inactive.
    Example: Consider a feature from samples A (active) and I (inactive).
    If (feature A/feature I) >= 10, consider active. 
    The factor can be user-provided.  
    
    This logic works only if:
    -same injection volume was used for all sample in mass spec analysis
    -samples in bioactivity analysis were in the same dilution as in
    mass spec analysis
    """
    #tests if a bioactivity csv was provided; if not = False
    if bioactivity_samples == False:
        return list()
    
    #active samples
    features_from_actives = dict()
    for active_sample in bioactivity_samples["active"]:
        for index, row in samples[active_sample].iterrows():
            feature_ID = row["feature_ID"]
            intensity = float(row["intensity"])
            #tests if feature_ID is already in dict
            if feature_ID in features_from_actives:
                #keeps the lowest intensity
                if features_from_actives[feature_ID] > intensity:
                    features_from_actives[feature_ID] = intensity
            #assigns feature_ID to dictionary
            else:
                features_from_actives[feature_ID] = intensity
    
    #inactive samples
    features_from_inactives = dict()
    for inactive_sample in bioactivity_samples["inactive"]:
        for index, row in samples[inactive_sample].iterrows():
            feature_ID = row["feature_ID"]
            intensity = float(row["intensity"])
            #tests if feature_ID is already in dict
            if feature_ID in features_from_inactives:
                #keeps the highest intensity
                if features_from_inactives[feature_ID] < intensity:
                    features_from_inactives[feature_ID] = intensity
            #assigns feature_ID to dictionary
            else:
                features_from_inactives[feature_ID] = intensity

    #list of bioactivity-associated features
    list_bioactivity_associated = []
    for feature_ID in features_from_actives:
        if feature_ID not in features_from_inactives:
            list_bioactivity_associated.append(feature_ID)
        else:
            #If intensity of feature from active sample is n times 
            #higher than intensity of feature from inactive sample,
            #consider True
            if (features_from_actives[feature_ID]
            / features_from_inactives[feature_ID]) > bioact_factor:
                list_bioactivity_associated.append(feature_ID)
    #add to feature objects
    for feature_ID in list_bioactivity_associated:
        feature_objects[feature_ID].bioactivity_associated = True
    return list_bioactivity_associated
    
    


