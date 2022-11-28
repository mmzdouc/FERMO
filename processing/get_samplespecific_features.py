import pandas as pd

def get_samplespecific_features(peaktable, sample_stats, filter_range):
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
    samples : `dict`
        Sample_names(keys) : pandas.core.frame.DataFrame(values)
        
    Notes
    -------
    Initializes new pandas dataframe per sample, to store
    sample-specific information
    Calculates start and stop of each peak.
    """

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
        
        #remove features with a norm_intensity outside of user-provided range
        sample_df = sample_df.loc[
            (sample_df['norm_intensity'] >= filter_range[0])
            &
            (sample_df['norm_intensity'] <= filter_range[1])
            ]
        
        #reset index
        sample_df.reset_index(drop=True, inplace=True)
        
        #pull the list of features per sample and store in sample_stats
        sample_stats["features_per_sample"][sample_name] = (
            sample_df.loc[:,"feature_ID"].tolist()
            )
        #assign to dict
        samples[sample_name] = sample_df
        
    return samples
