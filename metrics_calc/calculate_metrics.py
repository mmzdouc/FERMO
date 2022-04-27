import pandas as pd

from .get_samplespecific_features import get_samplespecific_features
from .calculate_feature_overlap import calculate_feature_overlap
from .filter_for_topn_features import filter_for_topn_features
from .determine_bioactive_features import determine_bioactive_features
from .calculate_feature_score import calculate_feature_score
from .determine_blank_features import determine_blank_features


def calculate_metrics(
peaktable : str, 
feature_objects : dict,
bioactivity_samples: dict,
attributes_samples: dict,
strictness_min: float, 
strictness_ppm: float,
topn: float,
bioact_factor: int,
column_bleed_factor: int,
convolutedness_weight : float,
bioactivity_weight : float,
novelty_weight : float, 
diversity_weight : float) -> dict:
    """Calculate metrics for samples and score them:
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    bioactivity_samples : `dict`
        contains two lists (active, inactive) of samples generated
        by function importing.read_from_bioactiv_table
    attributes_samples : `dict`
        contains two lists (samples, blanks) of samples generated
        by function importing.read_from_metadata_table
    strictness_min : `float`
        In minutes. Artificially increases width of peak to 
        detect overlaps more sensitively.
    strictness_ppm : `float`
        Tolerable mass deviation in ppm. Allows to tweak precision of
        matching. Should be matched to precision of instrument. E.g.
        20 ppm is still tolerable
    topn : `float`
        Float between 0 and 1. Is the quantile of features that is 
        retained. E.g. 0.9 means: 90th quantile -> remove features 
        that have a relative intensity of less than 0.1 of feature 
        with highest intensity (1.0).
    bioact_factor : `int`
        factor to determine if a feature, detected in both an active
        and an inactive sample, can be considered to be bioactivity
        associated
    column_bleed_factor : `int`
        factor to determine if a feature, detected in both a sample
        and a blank, can be not considered a blank-associated feature
    convolutedness_weight : `float`
        Determines how much points/weight is given to convoluteness
    bioactivity_weight : `float`
        Determines how much points/weight is given to bioactivity
    bioactivity_novelty : `float`
        Determines how much points/weight is given to novelty
    diversity_weight : `float`
        Determines how much points/weight is given to diversity
        
    Returns
    -------
    samples : `dict`
        Sample_names(keys):pandas.core.frame.DataFrame(values)
    
    Notes
    -----
    Extracts sample-specific features
    Filters sample-specific features for topN features
    Calculates feature overlap per sample
    Detects bioactivity-associated features
    ...
    Calculates scores for samples
    """
    #creates dataframes for each sample
    samples = get_samplespecific_features(peaktable, strictness_min)
    #Filter for top 95% of ft reg relative int to ft with highest int
    samples = filter_for_topn_features(samples, topn)
    #Calculates overlap of features; contains adduct/duplicate info
    samples = calculate_feature_overlap(samples, strictness_ppm)
    #calculates associated bioactivity yes/no
    bioactivity_associated_features = determine_bioactive_features(
    bioactivity_samples, samples, feature_objects, bioact_factor)
    #calculates associated medium/blank yes/no
    blank_associated_features = determine_blank_features(
    attributes_samples, samples, feature_objects, column_bleed_factor)
    
    
    
    
    ###CALCULATION SCORES
    #temporary score: 
    sample_count = dict()
    for sample in samples:
        #collect feature points per sample
        feature_list = list()
        convolutedness = list()
        bioactivity = list()
        novelty = list()
        diversity = list()
        n_features_per_sample = int(len(samples[sample]))
        for index, row in samples[sample].iterrows():
            feature_list.append(int(row["feature_ID"])) 
            #calculation of score per feature
            feature_points = calculate_feature_score(
            row, feature_objects, n_features_per_sample,
            convolutedness_weight, bioactivity_weight, novelty_weight, 
            diversity_weight)
            convolutedness.append(feature_points[0])
            bioactivity.append(feature_points[1])
            novelty.append(feature_points[2])
            diversity.append(feature_points[3])
        #appends lists to existing dataframe
        samples[sample]['convolutedness_score'] = convolutedness
        samples[sample]['bioactivity_score'] = bioactivity
        samples[sample]['novelty_score'] = novelty
        samples[sample]['diversity_score'] = diversity
        #create a combined score
        samples[sample]["combined_score"] = samples[sample].loc[:,[
        'convolutedness_score',
        'bioactivity_score',
        'novelty_score', 
        'diversity_score']].sum(axis=1)
        #sorts after "combined score" from high to low
        samples[sample].sort_values(by=["combined_score"], 
        inplace=True, ascending=False)
        #resets index just to clean up
        samples[sample].reset_index(drop=True, inplace=True)
    ###
    return samples

