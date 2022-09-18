import pandas as pd

def determine_bioactive_features(
    bioactivity_samples,
    samples,
    feature_dicts,
    bioact_factor,
    sample_stats,
    filename):
    """Determine bioactivity-associated features, append to feature dicts.
    
    Parameters
    ----------
    bioactivity_samples : `Pandas.DataFrame`
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    bioact_factor : `int`
        factor to determine if a feature, detected in both an active
        and an inactive sample, can be considered to be bioactivity
        associated
    sample_stats : `dict`
        dict containing general info on dataset, inclucing sample list
    filename : `str` or `None`
    
    Notes
    -----
    Compares set of features from bioactive samples against set
    of features from inactive samples (non-redundant).
    
    For features from active samples, keep the lowest intensity.
    For features from inactive samples, keep the highest intensity.
    
    If a feature is found only in active samples, count it as an 
    activity-associated feature.
    If a feature is found in both an active and an inactive sample,
    compare the intensities: the minimum intensity detected
    for activity, and the maximum intensity detected for inactivity. 
    If the minimum active intensity is n times higher (e.g. 5)
    than the maximum inactive intensity, count as an activity-associated
    feature. Else, consider inactive.
    
    Example: 
        Consider a feature from samples A (active) and I (inactive).
        If (feature A/feature I) >= 10, consider active. 
        
    Limitations:
    Logic is valid only if:
    -same injection volume was used for all sample in mass spec analysis
    -samples in bioactivity analysis were in the same dilution as in
    mass spec analysis.
    
    Also, the bioactivity value per sample is stored in the
    "list_bioactivities" attribute in the Feature Objects, 
    following sorting of "presence_samples" attribute.
    """
    #tests if bioactivity was provided
    if filename is not None:

        set_active_samples = sample_stats['active_samples_set']
        set_inactive_samples = sample_stats['inactive_samples_set']

        #features from active samples
        features_actives = dict()
        for active_sample in set_active_samples:
            #extract the lowest intensity per feature
            for index, row in samples[active_sample].iterrows():
                feature_ID = row["feature_ID"]
                intensity = float(row["intensity"])
                #tests if feature_ID is already in dict
                if feature_ID in features_actives:
                    #keeps the lowest intensity
                    if features_actives[feature_ID] > intensity:
                        features_actives[feature_ID] = intensity
                #assigns feature_ID to dictionary
                else:
                    features_actives[feature_ID] = intensity
        
        #features from inactive samples
        features_inactives = dict()
        for inactive_sample in set_inactive_samples:
            for index, row in samples[inactive_sample].iterrows():
                feature_ID = row["feature_ID"]
                intensity = float(row["intensity"])
                #tests if feature_ID is already in dict
                if feature_ID in features_inactives:
                    #keeps the highest intensity
                    if features_inactives[feature_ID] < intensity:
                        features_inactives[feature_ID] = intensity
                #assigns feature_ID to dictionary
                else:
                    features_inactives[feature_ID] = intensity

        #list of bioactivity-associated features
        list_bioactiv_associated = []
        for feature_ID in features_actives:
            if feature_ID not in features_inactives:
                list_bioactiv_associated.append(feature_ID)
            else:
                #If intensity of feature from active sample is n times 
                #higher than intensity of feature from inactive sample,
                #consider True
                if (features_actives[feature_ID]
                / features_inactives[feature_ID]) > bioact_factor:
                    list_bioactiv_associated.append(feature_ID)
        
        #for each bioactivity-associated feature
        for feature_ID in list_bioactiv_associated:
            #if not detected in a blank/medium blank
            if feature_dicts[feature_ID]['blank_associated'] == False:
                
                #collect samples in which feature was found
                presence_samples = feature_dicts[feature_ID]['presence_samples']

                list_bioactivities = list()
                #for each sample in which feature was detected, 
                #pull the bioactivity-value from bioactivity_samples
                #and assign to Feature Object
                for sample in presence_samples:
                    try: list_bioactivities.append(
                            bioactivity_samples.loc[
                                bioactivity_samples["sample_name"] == sample, 
                                "bioactivity"].item()
                        )
                    except ValueError:
                        list_bioactivities.append(0)
                
                #Append to Feature Objects
                feature_dicts[feature_ID]['bioactivity_samples'] = list_bioactivities
                feature_dicts[feature_ID]['bioactivity_associated'] = True

            else:
                feature_dicts[feature_ID]['bioactivity_associated'] = False
    else:
        pass
