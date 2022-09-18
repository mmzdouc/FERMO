import pandas as pd
import numpy as np

def calculate_feature_score(
    row, 
    feature_dicts,
    samples,
    sample,):
    """Calculate points for each feature.
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    samples : `dict`
    sample : `str`

    Returns
    -------
    `dict`
    
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
    ...
    D) NOVELTY:
    Scores novelty of a feature (comparison against external data)
    Based on comparison against spectral library and MS2Query.
    ...
    F) BLANK-ASSOCIATEDNESS:
    Medium- or blank- associatedness means that feature is not 
    interesting for drug discovery. Discard.
    If medium-associated, set to True; else to False
    """
    
    #RELATIVE INTENSITY
    rel_intensity_point = rel_intensity(row)
    #CONVOLUTEDNESS
    convolutedness_point = convolutedness(row, samples, sample)
    
    #BIOACTIVITY
    bioactivity_point = bioactivity(row, feature_dicts)

    #NOVELTY
    novelty_point = novelty(row, feature_dicts, samples, sample)
    
    #BLANK-ASSOCIATEDNESS
    blank_associatedness = in_blank(row, feature_dicts)
    
    #CALCULATION
    return {
        'rel_intensity_p' : rel_intensity_point,
        'convolutedness_p' : convolutedness_point,
        'bioactivity_p' : bioactivity_point,
        'novelty_p' : novelty_point,
        'blank_ass' : blank_associatedness,
        }


def novelty(
    row, 
    feature_dicts, 
    samples, 
    sample):
    '''Calculate novelty score
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    samples : `dict`
    sample : `str`

    Returns
    -------
    feature_points = `list`
    
    Notes
    -----
    Calculate potential novelty of feature (comparison to external data).
    
    Based on library search and/or MS2Query.
    
    If a feature is a common compound, it should be present in public
    reference data.
    Two kind of reference data are accessed: 
    -a spectral library in the .mgf-format (user-provided)
    -the libraries used by MS2Query (automated)

    
    If a compound is not found in the GNPS spectral library nor receives
    a high score in the comparison against the MS2Query embedding,
    it is probably something fairly uncommon.
    
    Comment regarding MS2Query scores: Personal communication
    with Niek de Jonge (MS2Query developer): 
    score > 0.95: very good
    0.4 < score <= 0.95: twilight zone;
    score < 0.4: unreliable
    '''
    
    feature_ID = int(row["feature_ID"])
    
    
    if (feature_dicts[feature_ID]['ms2spectrum'] is not None
        and not feature_dicts[feature_ID]['blank_associated']):
        
        if (
        ((feature_dicts[feature_ID]['cosine_annotation'])
        and
        (feature_dicts[feature_ID]['cosine_annotation_list'][0]['score'] >= 0.95))
        or
        ((feature_dicts[feature_ID]['ms2query'])
        and
        (feature_dicts[feature_ID][
            'ms2query_results'][0]['ms2query_model_prediction'] >= 0.95))
        ):
        #If modified cosine or MS2Query matching yielded a reliable 
        #match, set to 0
            return 0
        

        elif (
        (feature_dicts[feature_ID]['cosine_annotation'])
        and
        (0.80 <= feature_dicts[feature_ID]['cosine_annotation_list'][0]['score'] < 0.95)
        ):
        #If modified cosine 
        #yielded a non-reliable match (0.8 <= x < 0.95), 
        #set to value between 0.1 and 0.9
            x = feature_dicts[feature_ID]['cosine_annotation_list'][0]['score']
            x = round((
                ((x - 0.8) / 0.15) *
                (1 - 0.1) + 
                0.1
            ), 3)
            return (1 - x)
        
        elif (
        (feature_dicts[feature_ID]['ms2query'])
        and
        0.4 <= feature_dicts[feature_ID][
            'ms2query_results'][0]['ms2query_model_prediction'] < 0.95
        ):
        #If MS2Query matching  
        #yielded a non-reliable match (0.85 <= x < 0.95), 
        #set to value between 0.1 and 0.9
            x = float(feature_dicts[feature_ID][
                'ms2query_results'][0]['ms2query_model_prediction'])
            x = round((
                ((x - 0.4) / 0.55) *
                (1 - 0.1) + 
                0.1
            ), 3)
            return (1 - x)
            
        else:
        #Probably novel
            return 1
    else:
    #not eligible
        return 0

def rel_intensity(row): 
    """Extracts relative intensity information."""
    return float(row["norm_intensity"])

def bioactivity(
    row, 
    feature_dicts
    ):
    """Extracts bioactivity information."""
    
    if feature_dicts[int(row["feature_ID"])]['bioactivity_associated'] == True:
        bioactivity_samples = feature_dicts[
            int(row["feature_ID"])]['bioactivity_samples']
        return max(bioactivity_samples)
    else: 
        return 0

def in_blank(
    row,
    feature_dicts,
    ):
    """Extracts blank-associatedness information."""
    
    if feature_dicts[int(row["feature_ID"])]['blank_associated'] == True:
        return True
    else: 
        return False

def convolutedness(
    row, 
    samples, 
    sample,
    ):
    """Calculates convolutedness: how much % of peak remains."""
    
    A_s = float(row["rt_start"])
    A_e = float(row["rt_stop"])
    #at beginning of calculation, A_rt_remainder and A_rt_full are equal
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
    try:
        return (A_rt_remainder / A_rt_full)
    except ZeroDivisionError:
        return 0

def calculate_metrics(samples, feature_dicts,):
    """Calculate metrics for samples and score them:
    
    Parameters
    ----------
    samples : `samples`
        sample_names(keys):pandas.core.frame.DataFrame(values)
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)

    Returns
    -------
    samples : `dict`
        sample_names(keys):pandas.core.frame.DataFrame(values)
    
    Notes
    -----
    Extracts sample-specific features
    Filters sample-specific features for topN features
    Calculates feature overlap per sample
    Detects bioactivity-associated features
    Detects blank-associated features
    ...
    Calculates scores for samples
    """

    ###CALCULATION SCORES

    sample_count = dict()
    #for each sample
    for sample in samples:
        #collect feature scores per sample
        feature_list = list()
        rel_intensity = list()
        convolutedness = list()
        bioactivity = list()
        novelty = list()
        diversity = list()
        blank_associatedness = list()
        ms1_only = list()
        
        #for each feature in sample
        for id, row in samples[sample].iterrows():
            feature_list.append(int(row["feature_ID"])) 
            
            #calculation of score per feature
            feature_scores = calculate_feature_score(
                row, 
                feature_dicts, 
                samples, 
                sample)
                
            #appending to lists
            rel_intensity.append(feature_scores['rel_intensity_p'])
            convolutedness.append(feature_scores['convolutedness_p'])
            bioactivity.append(feature_scores['bioactivity_p'])
            novelty.append(feature_scores['novelty_p'])
            blank_associatedness.append(feature_scores['blank_ass'])
            
            #additional row to append info is ms2 available
            if feature_dicts[int(row["feature_ID"])]['ms2spectrum'] is None: 
                ms1_only.append(True)
            else:
                ms1_only.append(False)
        #appends lists to existing dataframe
        samples[sample]['rel_intensity_score'] = rel_intensity
        samples[sample]['convolutedness_score'] = convolutedness
        samples[sample]['bioactivity_score'] = bioactivity
        samples[sample]['novelty_score'] = novelty
        samples[sample]['in_blank'] = blank_associatedness
        samples[sample]['over_threshold'] = False
        samples[sample]['ms1_only'] = ms1_only
        
    return samples

