import pandas as pd
import copy

def collect_stats_samples(peaktable, groups, bioactivity_samples,):
    """Extracts and concatenate sample stats
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    groups : `dict`
    bioactivity_samples : `pandas.core.frame.DataFrame`

    Returns
    -------
    sample_stats : `dict`
    
    Notes
    ------
    samples_list : list of all samples
    samples_dict : dict of all samples with their associated group
    groups_dict : dict of all groups, with associated samples
    
    """
    rt_min = min(peaktable.loc[:,"retention_time"])
    rt_max = max(peaktable.loc[:,"retention_time"])
    rt_range = (rt_max - rt_min)
    
    #Get names of samples by mining peaktable columns
    samples_set = set()
    for label in peaktable.filter(regex=":intensity_range:max").columns:
        samples_set.add(label.split(":")[1])
    
    #AD BIOACTIVITY
    #If bioactivity was provided, test if 'active' samples exist in samples_set
    #If no bioactivity provided, all samples are set as 'inactive'
    try:
        active_samples_set = set(bioactivity_samples.loc[:,'sample_name'])
        inactive_samples_set = copy.deepcopy(samples_set)
        for active_sample in active_samples_set.copy():
            if not active_sample in samples_set:
                active_samples_set.remove(active_sample)
        
        for active_sample in active_samples_set:
            inactive_samples_set.remove(active_sample)
    except:
        active_samples_set = set()
        inactive_samples_set = copy.deepcopy(samples_set)
    
    #AD GROUPS (METADATA)
    #Test if all samples have been assigned their groups;
    #If any unassigned samples, assign to reserved group "GENERAL
    grouped_samples_set = set()
    for group in groups:
        for sample in groups[group].copy():
            if sample in samples_set:
                grouped_samples_set.add(sample)
            else:
                groups[group].remove(sample)
    for i in samples_set.difference(grouped_samples_set):
        groups['GENERAL'].add(i)
    
    #create a dict of samples with group info attached
    samples_list = list(samples_set)
    samples_dict = {}
    for sample in samples_list:
        for group in groups:
            if sample in groups[group]:
                samples_dict[sample] = group
    
    sample_stats = {
        "rt_min" : rt_min, 
        "rt_max" : rt_max,
        "rt_range" : rt_range,
        "samples_list" : samples_list,
        "samples_dict" : samples_dict,
        "groups_dict" : groups,
        "features_per_sample" : {},
        "cliques_per_sample" : {},
        "cliques" : {},
        "nr_all_cliques" : "",
        "set_all_cliques" : set(),
        "set_blank_cliques" : set(),
        "active_samples_set" : active_samples_set,
        "inactive_samples_set" : inactive_samples_set,
        'relative_intensity_removed_features' : [],
        }
    return sample_stats
