import pandas as pd
import numpy as np

from .get_samplespecific_features import get_samplespecific_features
from .calculate_feature_overlap import calculate_feature_overlap
from .filter_for_topn_features import filter_for_topn_features
from .determine_bioactive_features import determine_bioactive_features
from .determine_blank_features import determine_blank_features
from .calculate_feature_score import calculate_feature_score



def calculate_metrics(
peaktable : str, 
feature_objects : dict,
bioactivity_samples: dict,
attributes_samples: dict,
args : str) -> dict:
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
    args : `argparse object`
        contains all user-provided args

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
    Detects blank-associated features
    ...
    Calculates scores for samples
    """
    #creates dataframes for each sample
    samples = get_samplespecific_features(peaktable, args.strictness_min)
    #Filter for top n% of ft reg relative int to ft with highest int
    samples = filter_for_topn_features(samples, args.feature_retain_factor)
    #Calculates overlap of features; contains adduct/duplicate info
    samples = calculate_feature_overlap(samples, args.strictness_ppm)
    #calculates associated bioactivity yes/no
    bioactivity_associated_features = determine_bioactive_features(
    bioactivity_samples, samples, feature_objects, args.bioactivity_factor)
    #calculates associated medium/blank yes/no
    blank_associated_features = determine_blank_features(
    attributes_samples, samples, feature_objects, args.column_bleed_factor)
    
    
    
    
    ###CALCULATION SCORES

    sample_count = dict()
    for sample in samples:
        #collect feature points per sample
        feature_list = list()
        rel_intensity = list()
        convolutedness = list()
        bioactivity = list()
        novelty = list()
        diversity = list()
        
        #for each sample
        for index, row in samples[sample].iterrows():
            feature_list.append(int(row["feature_ID"])) 
            #calculation of score per feature
            feature_points = calculate_feature_score(
            row, feature_objects, samples, sample)
            #appending to lists
            rel_intensity.append(feature_points[0])
            convolutedness.append(feature_points[1])
            bioactivity.append(feature_points[2])
            novelty.append(feature_points[3])
            diversity.append(feature_points[4])

        #appends lists to existing dataframe
        samples[sample]['rel_intensity_score'] = rel_intensity
        samples[sample]['convolutedness_score'] = convolutedness
        samples[sample]['bioactivity_score'] = bioactivity
        samples[sample]['novelty_score'] = novelty
        samples[sample]['diversity_score'] = diversity
        
        
        #Check if bioactivity table was provided; if yes, check across 
        #3 values, else only across 2
        if args.bioactivity: 
            #check across rel_int, convolutedness, bioactivity
            #expand once scores are implemented
            condition = [
            samples[sample]['rel_intensity_score'].ge(args.rel_intensity_threshold) &
            samples[sample]['convolutedness_score'].ge(args.convolutedness_threshold) &
            samples[sample]['bioactivity_score'].ge(args.bioactivity_threshold)]
            choice = [True]
            samples[sample]['over_threshold'] = np.select(
            condition, choice, default=False)
        else:
            #check across rel_int and convolutedness
            condition = [
            samples[sample]['rel_intensity_score'].ge(args.rel_intensity_threshold) &
            samples[sample]['convolutedness_score'].ge(args.convolutedness_threshold)]
            choice = [True]
            samples[sample]['over_threshold'] = np.select(
            condition, choice, default=False)

        #sorts after "over_threshold", Trues on top
        samples[sample].sort_values(
        by=["over_threshold",
        "rel_intensity_score",
        "convolutedness_score",
        "bioactivity_score",
        "novelty_score",
        "diversity_score"
        ], 
        inplace=True, 
        ascending=[False, False, False, False, False, False])
        #resets index just to clean up
        samples[sample].reset_index(drop=True, inplace=True)
        
        #TESTING, DELETE LATER
        # ~ print(sample)
        # ~ print(samples[sample][["feature_ID", "precursor_mz", "retention_time",
        # ~ 'rel_intensity_score', 'convolutedness_score', 'bioactivity_score',
         # ~ 'over_threshold']])
    
    ###
    return samples

