import pandas as pd
import statistics

def determine_blank_features(
    samples,
    feature_dicts,
    column_ret_factor,
    sample_stats):
    """Determines blank-associated features.
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    column_ret_factor : `int`
        factor to determine if a feature, detected in both a sample
        and a blank, can be not considered a blank-associated feature
    sample_stats : `dict`
        dict containing general info on dataset, inclucing sample list

    Notes
    -----
    Compares set of features from blank/medium samples against set
    of features from regular samples (non-redundant).
    
    For each non-redundant feature, calculate the median intensity
    across blanks and across regular samples. 
    
    If a feature is found only in blanks, count it as an 
    blank-associated feature.
    
    If a feature is found in both a regular sample and a blank,
    compare the median intensities: 
        If the median intensity in regular samples is n times 
        higher (e.g. 10) than the maximum across blanks, 
        do not count as an blank-associated feature. 
        Else, consider it a blank-associated feature.
        
    This logic takes into account the occurrence of column retention 
    and bleed, which can lead to cross-contamination of intense sample
    peaks into the blanks. If simply all features occurring in blanks
    would be excluded, it would also hit such high-intensity sample
    peaks, which is bad. 
    This assumes that medium components have a similar abundance
    in both sample and blanks, and it assumes that
    cross-contaminating peaks have a much lower abundance in blanks 
    than in the regular samples (provided that both regular samples 
    and medium blanks were extracted and prepared in an identical way).
    
    Example: Consider two features A and B, present in both regular
    samples and blanks. Feature A has a median intensity of 5000 across
    regular samples and a maximum of 5500 in the blank. 
    Feature B has a medium intensity of 50000 across regular samples 
    and a maximum of 500 in the blank. 
    It is very likely that feature A is a medium component, while 
    feature B is a sample analyte that has been retained by the column
    and bleeds into the blank.
    """
    #Test if a metadata file was provided: if not, BLANK is not available
    try:
        if sample_stats['groups_dict']['BLANK']:

            #"^" operator extracts differents between sets (not in both)
            set_samples = (
                set(sample_stats["samples_list"])
                ^
                sample_stats['groups_dict']['BLANK'])
            
            #regular samples
            features_from_samples = dict()
            for regular_sample in set_samples:
                for id, row in samples[regular_sample].iterrows():
                    feature_ID = row["feature_ID"]
                    intensity = float(row["intensity"])
                    
                    #tests if feature_ID is already in dict
                    if feature_ID in features_from_samples:
                        features_from_samples[feature_ID].append
                    #assigns feature_ID to dictionary
                    else:
                        features_from_samples[feature_ID] = [intensity]
            
            #blanks
            features_from_blanks = dict()
            for blank in sample_stats['groups_dict']['BLANK']:
                for id, row in samples[blank].iterrows():
                    feature_ID = row["feature_ID"]
                    intensity = float(row["intensity"])
                    
                    #tests if feature_ID is already in dict
                    if feature_ID in features_from_blanks:
                        features_from_blanks[feature_ID].append
                    #assigns feature_ID to dictionary
                    else:
                        features_from_blanks[feature_ID] = [intensity]

            #list of blank-associated features
            blank_associated_features = []
            for feature_ID in features_from_blanks:
                if feature_ID not in features_from_samples:
                    blank_associated_features.append(feature_ID)
                else:
                    #Considers column bleed. For logic, see above in "Notes"
                    if not (
                        (statistics.median(features_from_samples[feature_ID])
                    / 
                        max(features_from_blanks[feature_ID])) 
                    >
                    column_ret_factor):
                        blank_associated_features.append(feature_ID)

            #add to feature objects
            for feature_ID in blank_associated_features:
                feature_dicts[feature_ID]['blank_associated'] = True
    except KeyError:
        pass
