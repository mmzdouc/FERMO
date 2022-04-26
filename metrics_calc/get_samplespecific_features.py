import pandas as pd


def get_samplespecific_features(peaktable: str, 
strictness_min: float) -> dict[str, pd.DataFrame]:
    """Extract sample names, associated features and their intensities
    from peaktable.
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    strictness_min : `float`
        In minutes. Artificially increases width of peak to 
        detect overlaps more sensitively.
    
    Returns
    -------
    samples : `dict`
        Sample_names(keys):pandas.core.frame.DataFrame(values)
        
    Notes
    -------
    Creates sample-specific feature table for downsteam calculation 
    of complexity metrics.
    Includes feature_ID, intensity, retention_time, normalized_int.
    Also calculates start and stop of each peak and adds "strictness"
    in minutes, which makes the peak artificially wider.
    Scrapes sample names from peaktable -> no user input is needed
    """
    #MZmine3 table SIMPLE
    if not peaktable.filter(regex="Peak").empty:
        samples = dict()
        
        #test for field to scrape sample names from
        assert not peaktable.filter(
        regex=".mzML|.mzXML").columns.empty, \
        """
        WARNING: Could not find cloumns with 
        '.mzML|.mzXML' which is used to collect sample names. 
        Did the Mzmine3 output format change? 
        Contact the FERMO developers."""
        
        for label in peaktable.filter(regex=".mzML|.mzXML").columns:
            #get name of sample
            sample_name = label.split(" ")[0]
            sample_dataframe = peaktable[["feature_ID", "precursor_mz",
            "retention_time", label]].loc[peaktable[label] != 0]
            #rename
            sample_dataframe.rename({label : "intensity"}, axis=1, 
            inplace=True)
            #create fwhm column (fake values)
            sample_dataframe["fwhm"] = 0.2
            #min-max-normalization intensity
            sample_dataframe = min_max_norm(sample_dataframe, "intensity")
            #add start_stop_rt
            sample_dataframe = calc_start_stop_rt(
            sample_dataframe, "retention_time", "fwhm", strictness_min)
            #reset index
            sample_dataframe.reset_index(drop=True, inplace=True)
            #assign to dict
            samples[sample_name] = sample_dataframe
        return samples
    #MZmine3 table ALL
    elif not peaktable.filter(regex="^datafile:").empty:
        samples = dict()
        
        #test for field to scrape sample names from
        assert not peaktable.filter(
        regex=":intensity_range:max").columns.empty, \
        """
        WARNING: Could not find cloumns with 
        'SAMPLE:intensity_range:max' which is used
        to collect sample names. Did the Mzmine3 output
        format change? Contact the FERMO developers."""
        
        #finds file names via lable ":intensity_range:max", chosen
        #since there is only one such field per row, can be changed
        for label in peaktable.filter(regex=
        ":intensity_range:max").columns:
            #get name of sample
            sample_name = label.split(":")[1]
            #construct fwhm column name 
            sample_fwhm = ''.join(["datafile:", sample_name, ":fwhm"])
            #extract sample-specific features
            sample_dataframe = peaktable[[
            "feature_ID", "precursor_mz", "retention_time", 
            sample_fwhm, label]].dropna()
            #rename
            sample_dataframe.rename({label : "intensity",
            sample_fwhm : "fwhm" }, axis=1, 
            inplace=True)
            #min-max-normalization intensity
            sample_dataframe = min_max_norm(sample_dataframe, "intensity")
            #add start_stop_rt
            sample_dataframe = calc_start_stop_rt(
            sample_dataframe, "retention_time", "fwhm", strictness_min)
            #reset index
            sample_dataframe.reset_index(drop=True, inplace=True)
            #assign to dict
            samples[sample_name] = sample_dataframe
        return samples
    
    #Should give a clear error message if input format has changed
    else:
        #test for field to scrape sample names from
        assert not peaktable.filter(
        regex=".mzML|.mzXML").columns.empty, \
        """
        WARNING: Could not find cloumns with 
        '.mzML|.mzXML' which is used to collect sample names. 
        Did the Mzmine3 output format change? 
        Contact the FERMO developers."""
        #test for field to scrape sample names from
        assert not peaktable.filter(
        regex=":intensity_range:max").columns.empty, \
        """
        WARNING: Could not find cloumns with 
        'SAMPLE:intensity_range:max' which is used
        to collect sample names. Did the Mzmine3 output
        format change? Contact the FERMO developers."""
        raise KeyError

def min_max_norm(df, col_name):
    """Perform a min max normalisation.
    
    Parameters
    ----------
    df : `pandas.core.frame.DataFrame`
    col_name : `str`
        column name to min max normalize
        
    Returns
    -------
    new_df : `pandas.core.frame.DataFrame`
    """
    #performs min_max_norm on column of floats
    min_max_norm = df[col_name].apply(
    lambda x: ((x - df[col_name].min()) / 
    (df[col_name].max() - (df[col_name].min()))))
    #renames column
    min_max_norm.rename(''.join(["min_max_norm_", col_name]), 
    inplace=True)
    #concats df and new
    new_df = pd.concat([df, min_max_norm], axis=1)
    return new_df

def calc_start_stop_rt(df, col_rt, col_fwhm, strictness_min):
    """Calculate start and stop of peak.
    
    Parameters
    ----------
    df : `pandas.core.frame.DataFrame`
    col_rt : `str`
        column name with rt in minutes
    col_fwhm : `str`
        column name with fwhm in minutes
        
    Returns
    -------
    df : `pandas.core.frame.DataFrame`
    """
    #start peak
    df["rt_start"] = df.apply(
    lambda x: df[col_rt].loc[x.name] - 
    ((df[col_fwhm].loc[x.name]) * 0.5) - strictness_min, 
    axis=1)
    #stop peak
    df["rt_stop"] = df.apply(
    lambda x: df[col_rt].loc[x.name] + 
    ((df[col_fwhm].loc[x.name]) * 0.5) + strictness_min, 
    axis=1)
    return df
