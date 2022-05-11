import pandas as pd

def calculate_feature_score(row : str, 
feature_objects : dict,
samples : dict,
sample : str) -> list:
    """Calculate points for each feature.
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    samples : `dict`
    sample : `str`

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
    A)RELATIVE INTENSITY:
    Features with higher intensity can be considered more interesting 
    for isolation
    ...
    B) CONVOLUTEDNESS (crowdedness):
    A high number of non-overlapping, high-intensity features is 
    desirable.
    ...
    C) BIOACTIVITY:
    Bioactivity-association of feature generally considered good. 
    Not every experiment provides bioactivity, therefore optional.
    Currently binary, i.e. if bioactive, weight fully attributed to peak
    ...
    D) NOVELTY:
    TBA (needs more expensive calculations)
    ...
    E) DIVERSITY:
    TBA (needs more expensive calculations)
    """
    
    ##RELATIVE INTENSITY
    rel_intensity_point = 1.0 * float(
    row["min_max_norm_intensity"])
    
    ###CONVOLUTEDNESS
    ##retention_time_overlap_factor
    #assigns to variable to make equations easier to read
    A_s = float(row["rt_start"])
    A_e = float(row["rt_stop"])
    A_rt_remainder = (A_e - A_s)
    A_rt_full = A_rt_remainder
    #if there is a collision, follow up on how much of peak is affected
    if row["feature_collision"] == True:
        X_s_left = []
        X_e_left = []
        X_s_right = []
        X_e_right = []
        X_s_middle = []
        X_e_middle = []
        X_s_covered = []
        X_e_covered = []
        
        #checks for each collision that was registered
        for collision in row["feature_collision_list"]:
            #assigns to variable to make equations easier to read
            entry = samples[sample].loc[
            samples[sample]["feature_ID"] == collision]
            X_s = float(entry["rt_start"])
            X_e = float(entry["rt_stop"])
            #collects data to create "consensus overlaps"
            #if peak X is overlapping A on the left
            if (A_s >= X_s) and (A_e > X_e):
                X_s_left.append(X_s)
                X_e_left.append(X_e)
            #if peak X is overlapping A on the right
            if (A_s < X_s) and (A_e <= X_e):
                X_s_right.append(X_s)
                X_e_right.append(X_e)
            #if peak X is inside peak A (covered)
            if (A_s < X_s) and (A_e > X_e):
                X_s_middle.append(X_s)
                X_e_middle.append(X_e)
            #if peak A is inside peak X or identical(covered)
            if (A_s >= X_s) and (A_e <= X_e):
                X_s_covered.append(X_s)
                X_e_covered.append(X_e)
        
        #determine how much of peak remains
        #left side: check if there were overlaps: if, newly assigns A_s
        if X_e_left:
            A_s = max(X_e_left)
        #right side: check if there were overlaps: ifm newly assigns A_e
        if X_s_right: 
            A_e = min(X_s_right)
        #check if there is any peak rt is left after this step
        if A_s >= A_e:
            A_rt_remainder = 0
            pass
        else:
            A_rt_remainder = (A_e - A_s)
        
        #check if any X inside A
        if X_s_middle and X_e_middle:
            #stretches over both sides of the now reduced peak
            if min(X_s_middle) <= A_s and max(X_e_middle) >= A_e:
                A_rt_remainder = 0
                pass
            #X streches over left side
            elif min(X_s_middle) <= A_s and max(X_e_middle) < A_e:
                A_s = max(X_e_middle)
                A_rt_remainder = (A_e - A_s)
            #X streches over right side
            elif min(X_s_middle) > A_s and max(X_e_middle) >= A_e:
                A_e = min(X_s_middle)
                A_rt_remainder = (A_e - A_s)
            #X still inside A
            elif min(X_s_middle) > A_s and max(X_e_middle) < A_e:
                range_middle = max(X_e_middle) - min(X_s_middle)
                A_rt_remainder = A_rt_remainder - range_middle

        #check if any A inside X:
        if X_s_covered:
            A_rt_remainder = 0
            pass
    #makes the remainder of the rt a fraction of orignial rt of peak
    retention_time_overlap_factor = (A_rt_remainder / A_rt_full)
    
    ##blank associated factor
    blank_associated_factor = 1
    if feature_objects[int(row["feature_ID"])].blank_associated == True:
        blank_associated_factor = 0

    ##point calculation
    convolutedness_point = (
    1.0 * 
    retention_time_overlap_factor *
    blank_associated_factor)
    
    
    ###BIOACTIVITY
    #could be a bit more elaborated, currently only binary
    ##point calculation
    if feature_objects[
    int(row["feature_ID"])].bioactivity_associated == True and feature_objects[
    int(row["feature_ID"])].blank_associated == False:
        bioactivity_point = 1.0
    else:
        bioactivity_point = 0.0
        
    ###NOVELTY
    #expand; currently set to 0, does not influence metric
    ##point calculation
    novelty_point = 1.0 * 0
    
    ###DIVERSITY
    #expand; currently set to 0, does not influence metric
    ##point calculation
    diversity_point = 1.0 * 0
    
    
    ###CALCULATION
    feature_points = [
    rel_intensity_point,
    convolutedness_point,
    bioactivity_point,
    novelty_point,
    diversity_point]
    return feature_points
