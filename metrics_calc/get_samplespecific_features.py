import pandas as pd


def get_samplespecific_features(peaktable: str) -> dict[str, 
pd.DataFrame]:
    """Extract sample names, associated features and their intensities
    from peaktable.
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    
    Returns
    -------
    features : `dict`
        Sample_names(keys):pandas.core.frame.DataFrame(values)
        
    Notes
    -------
    Creates sample-specific feature table for downsteam calculation 
    of complexity metrics.
    Includes feature_ID, intensity, retention_time, normalized_int.
    """
    #MZmine3 table SIMPLE
    if not peaktable.filter(regex="Peak").empty:
        samples = dict()
        for label in peaktable.filter(regex=".mzML|.mzXML").columns:
            #get name of sample
            sample_name = label.split(" ")[0]
            sample_dataframe = peaktable[["feature_ID", 
            "retention_time", label]].loc[peaktable[label] != 0]
            #rename
            sample_dataframe.rename({label : "intensity"}, axis=1, 
            inplace=True)
            #create fwhm column (fake values)
            sample_dataframe["fwhm"] = 0.2
            #min-max-normalization intensity
            sample_dataframe = min_max_norm(sample_dataframe, "intensity")
            #assign to dict
            samples[sample_name] = sample_dataframe
        return samples
    #MZmine3 table ALL
    elif not peaktable.filter(regex="^datafile:").empty:
        samples = dict()
        for label in peaktable.filter(regex=
        ":intensity_range:max").columns:
            #get name of sample
            sample_name = label.split(":")[1]
            #construct fwhm column name 
            sample_fwhm = ''.join(["datafile:", sample_name, ":fwhm"])
            #extract sample-specific features
            sample_dataframe = peaktable[[
            "feature_ID", "retention_time", sample_fwhm, label
            ]].dropna()
            #rename
            sample_dataframe.rename({label : "intensity",
            sample_fwhm : "fwhm" }, axis=1, 
            inplace=True)
            #min-max-normalization intensity
            sample_dataframe = min_max_norm(sample_dataframe, "intensity")
            #assign to dict
            samples[sample_name] = sample_dataframe
        return samples
    else:
        raise KeyError

def min_max_norm(df, col_name):
    """Perform a min max normalisation.
    
    Parameters
    ----------
    df : `pandas.core.frame.DataFrame`
    series : `str`
        column name to min max normalize
        
    Returns
    -------
    features : `pandas.core.frame.DataFrame`
    """
    #performs min_max_norm on column of floats
    min_max_norm = df[col_name].apply(
    lambda x: ((x - df[col_name].min()) / 
    (df[col_name].max() - (df[col_name].min()))))
    #renames column
    min_max_norm.rename(''.join(["min_max_norm_", col_name]), 
    inplace=True)
    #concats df and new
    return pd.concat([df, min_max_norm], axis=1)

