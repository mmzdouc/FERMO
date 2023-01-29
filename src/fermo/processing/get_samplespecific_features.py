import numpy as np


def construct_sample_dict(
    peaktable,
    sample_stats,
    ):
    '''Return separate dataframe for each sample
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    sample_stats : `dict`
    
    Returns
    -------
    samples : `dict`
    '''
    samples = dict()

    for sample_name in sample_stats["samples_list"]:
        
        #Construct df column names for data retrieval
        sample_fwhm = ''.join(["datafile:", sample_name, ":fwhm"])
        sample_rt = ''.join(["datafile:", sample_name, ":rt"])
        max_intens = ''.join([
            "datafile:", 
            sample_name, 
            ":intensity_range:max"
            ])
        rt_start = ''.join([
            "datafile:", 
            sample_name, 
            ":rt_range:min"
            ])
        rt_stop = ''.join([
            "datafile:", 
            sample_name, 
            ":rt_range:max"
            ])
        
        #extract sample-specific features by using .dropna() method
        sample_df = peaktable.loc[:,
            ["feature_ID", 
            "precursor_mz", 
            sample_rt, 
            sample_fwhm, 
            max_intens,
            rt_start,
            rt_stop,]
            ].dropna()

        #rename column headers
        sample_df.rename({
            max_intens : "intensity",
            sample_rt : "retention_time",
            sample_fwhm : "fwhm",
            rt_start : "rt_start",
            rt_stop : "rt_stop"
            }, 
            axis=1, inplace=True)
        
        #add normalized intensity
        sample_df["norm_intensity"] = sample_df["intensity"].apply(
            lambda x: (
            (x - sample_df["intensity"].min()) / 
            (sample_df["intensity"].max() - sample_df["intensity"].min()))
            )
        
        #reset index
        sample_df.reset_index(drop=True, inplace=True)
        
        #assign to dict
        samples[sample_name] = sample_df
        
    return samples

def get_feature_int_range(
    samples,
    filter_range,
    ):
    '''Return dictionary with feature rel intensities across all samples
    
    Parameters
    ----------
    samples : `dict`
    
    Returns
    -------
    rel_int : `int`
    '''
    rel_int = dict()
    for sample in samples:
        zip_id_int = zip(
            list(samples[sample]['feature_ID']),
            list(samples[sample]['norm_intensity']),
            )
        
        for i in zip_id_int:
            if i[0] in rel_int:
                rel_int[i[0]].append(round(i[1],4))
            else:
                rel_int[i[0]] = []
                rel_int[i[0]].append(round(i[1],4))
    
    return rel_int


def get_features_inside_filter_range(
    rel_int,
    filter_range,
    ):
    '''Return set of features inside the filter range
    
    Parameters
    ----------
    rel_int : `dict`
    filter_range : `list`
    
    Returns
    -------
    included : `set`
    excluded : `set`
    '''
    included = set()
    excluded = set()
    
    for ID in rel_int:
        if (
        ( max(rel_int[ID]) >= filter_range[0] )
        and
        ( min(rel_int[ID]) <= filter_range[1] ) 
        ):
            included.add(ID)
        else:
            excluded.add(ID)
    
    return included, excluded
    


def get_samplespecific_features(
    peaktable,
    sample_stats,
    filter_range,
    ):
    """For each sample, extract features + info from peaktable
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    sample_stats : `dict`
    filter_range : `list`
        List with min and max; features must be inside the range 
        to be processed further
    
    Returns
    -------
    new_sample_dict : `dict`
        Sample_names(keys) : pandas.core.frame.DataFrame(values)
        
    Notes
    -------
    Initializes new pandas dataframe per sample, to store
    sample-specific information
    Calculates start and stop of each peak.
    """

    samples = construct_sample_dict(peaktable, sample_stats,)
    
    rel_int = get_feature_int_range(samples, filter_range)
    
    rel_int_included, rel_int_excluded = get_features_inside_filter_range(
        rel_int, 
        filter_range
        )
    
    for i in rel_int_excluded:
        sample_stats['relative_intensity_removed_features'].append(
            {i : rel_int[i]})
    
    rel_int_included_arr = np.array(list(rel_int_included))
    
    new_sample_dict = dict()
    for sample in samples:
        df = samples[sample].loc[
            samples[sample]['feature_ID'].isin(rel_int_included_arr)
            ]
        
        df.reset_index(drop=True, inplace=True)
        
        sample_stats["features_per_sample"][sample] = (
            df.loc[:,"feature_ID"].tolist()
            )

        new_sample_dict[sample] = df


    return new_sample_dict
