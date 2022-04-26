import pandas as pd
import re

def read_from_bioactiv_table(arg: str) -> list:
    """Read a bioactivity table and scrape names of active and inactive
    samples.
    
    Parameters
    ----------
    arg : `csv`
        Must be in format:
        sample_name,bioactivity
        sample1.mzML,inactive
        sample2.mzML,active

    Returns
    -------
    bioactivity_samples : `dict`
        Contains a list of active samples and a list of inactive samples
        
    Notes
    -------
    Currently, expects bioactivity table in binary format. 
    Allows for some flexibility regarding column names and indications
    for active/inactive.
    Once input formats are clearer, script can be adapted to
    interpret floats etc.
    """
    bioactiv_table = pd.read_csv(arg, sep=',')
    
    #ADD CHANGES TO REGEX QUERIES
    sample_col_list = ["sample", "sample_name"]
    bioactivity_col_list = ["activity", "bioactivity"]
    activity_true_list = ["^active$", "^true$", "^y$", "^yes$"]
    activity_false_list = ["^inactive$", "^false$", "^n$", "^no$"]
    
    #construction of regex-expressions to test column names
    sample_col_str = "|".join(sample_col_list)
    bioactivity_col_str = "|".join(bioactivity_col_list)
    #construction of regex-expressions to test field values
    activity_true_str = "|".join(activity_true_list)
    activity_false_str = "|".join(activity_false_list)
    
    #compiles regex objects to test column names
    sample_col_regex = re.compile(sample_col_str, flags=re.I)
    bioactivity_col_regex = re.compile(bioactivity_col_str, flags=re.I)
    #compiles regex objects to test field values
    activity_true_regex = re.compile(activity_true_str, flags=re.I)
    activity_false_regex = re.compile(activity_false_str, flags=re.I)
    
    #extracts column names for samples and bioactivity
    sample_col_query = bioactiv_table.filter(
    regex=sample_col_regex).columns
    bioactivity_col_query = bioactiv_table.filter(
    regex=bioactivity_col_regex).columns
    
    #verifies presence of column names for sample names and bioactivity
    assert not sample_col_query.empty, f""" 
    In input file {arg}, 
    could not find any column titled any of {*sample_col_list,}.
    Please check the formatting and try again."""
    assert not bioactivity_col_query.empty, f""" 
    In input file {arg}, 
    could not find any column titled any of {*bioactivity_col_list,}.
    Please check the formatting and try again."""
    
    #extracts list of actives w name stored in 
    #bioactivity_col_query and boolean mask
    active = bioactiv_table.loc[
    bioactiv_table.loc[:,bioactivity_col_query[0]
    ].str.contains(activity_true_regex)]
    #extracts list of inactives w bioactivity_col_query and boolean mask
    inactive = bioactiv_table.loc[
    bioactiv_table.loc[:,bioactivity_col_query[0]
    ].str.contains(activity_false_regex)]
    
    #formats to list using column name stored in sample_col_query
    active = active[sample_col_query[0]].to_list()
    inactive = inactive[sample_col_query[0]].to_list()
    
    #put into dictionary
    bioactivity_samples = {"active" : active, "inactive" : inactive}
    
    return bioactivity_samples
