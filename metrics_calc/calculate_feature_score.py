import pandas as pd

def calculate_feature_score(row : str, 
# ~ bioactivity_associated_features : list, 
feature_objects : dict,
n_features_per_sample : int):
    """Calculate points for each feature
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    # ~ bioactivity_associated_features : `list`
        # ~ List of features that are bioactivity-associated for 
        # ~ fast lookup
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    n_features_per_sample : `int`
    
    Returns
    -------
    feature_points = `list`
    
    Notes
    -----
    Features are scored based on how interesting they are from a natural
    product discovery point of view. 
    The more points a feature gets, the better.
    For each category, points are given.
    Details:
    A) CONVOLUTEDNESS (crowdedness):
    A high number of non-overlapping, high-intensity features is desirable.
    For each feature, a point is given, which is modified by a number 
    of factors:
    1) intensity factor: relative intensity of peak in sample
    2) overlap factor: if a overlap with non-adducts was detected,
    the number of overlaps with other peaks devided by the total number
    of peaks per sample is used as modifier (more features - more 
    overlaps)
    3) blank associated: if feature was found in a blank sample (medium
    or solvent), it is excluded
    ...
    B) BIOACTIVITY:
    Bioactivity-association of feature generally considered good. 
    Not every experiment provides
    ...
    C) NOVELTY:
    TBA (needs more expensive calculations)
    ...
    D) DIVERSITY:
    TBA (needs more expensive calculations)

    """
    ###CONVOLUTEDNESS
    ##factors
    #intensity factor
    intensity_factor = float(row["min_max_norm_intensity"])
    #overlap factor
    overlap_factor = 1
    if row["feature_collision"]:
        n_overlaps = len(row["feature_collision_list"])
        overlap_factor = (1 - (n_overlaps / n_features_per_sample))
    #blank associated factor
    blank_associated_factor = 1
    if feature_objects[int(row["feature_ID"])].blank_associated == True:
        blank_associated_factor = 0
    # ...
    ##point
    convolutedness_point = (
    1.0 * intensity_factor * overlap_factor * blank_associated_factor)
    
    ###BIOACTIVITY
    #could be a bit more elaborated, currently only binary
    ##point
    bioactivity_point = 0
    if feature_objects[int(row["feature_ID"])].bioactivity_associated == True:
        bioactivity_point = 1
    ###NOVELTY
    #expand; currently set to 0, does not influence metric
    ##point
    novelty_point = 0
    ###DIVERSITY
    #expand; currently set to 0, does not influence metric
    ##point
    diversity_point = 0
    
    ###CALCULATION
    feature_points = [
    convolutedness_point,
    bioactivity_point,
    novelty_point,
    diversity_point]
    return feature_points

