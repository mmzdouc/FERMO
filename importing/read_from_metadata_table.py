import pandas as pd
import re

def read_from_metadata_table(arg: str) -> list:
    """Read a metadata table and scrape names of samples and blanks.
    
    Parameters
    ----------
    arg : `csv`
        Must be in format:
        sample_name,sample_attribute
        sample1.mzML,sample
        sample2.mzML,(blank, medium, solvent, control)

    Returns
    -------
    blank_samples : `dict`
        Contains a list of samples and a list of blanks(solvent,medium)
        
    Notes
    -------
    In future, can be updated to accept more sample_attributes
    """
    metadata_table = pd.read_csv(arg, sep=',')
    
    #ADD CHANGES TO REGEX QUERIES
    sample_col_list = ["^sample$", "sample_name"]
    attribute_col_list = ["attribute", "sample_attribute"]
    attribute_true_list = ["sample"]
    attribute_false_list = ["blank", "medium", "solvent", "control"]
    
    #construction of regex-expressions to test column names
    sample_col_str = "|".join(sample_col_list)
    attribute_col_str = "|".join(attribute_col_list)
    #construction of regex-expressions to test field values
    attribute_true_str = "|".join(attribute_true_list)
    attribute_false_str = "|".join(attribute_false_list)
    
    #compiles regex objects to test column names
    sample_col_regex = re.compile(sample_col_str, flags=re.I)
    attribute_col_regex = re.compile(attribute_col_str, flags=re.I)
    #compiles regex objects to test field values
    attribute_true_regex = re.compile(attribute_true_str, flags=re.I)
    attribute_false_regex = re.compile(attribute_false_str, flags=re.I)
    
    #extracts column names for samples and blanks
    sample_col_query = metadata_table.filter(
    regex=sample_col_regex).columns
    attribute_col_query = metadata_table.filter(
    regex=attribute_col_regex).columns
    
    #verifies presence of column names for sample names and blanks
    assert not sample_col_query.empty, f""" 
    In input file {arg}, 
    could not find any column titled any of {*sample_col_list,}.
    Please check the formatting and try again."""
    assert not attribute_col_query.empty, f""" 
    In input file {arg}, 
    could not find any column titled any of {*attribute_col_list,}.
    Please check the formatting and try again."""
    
    #extracts list of samples w name stored in 
    #attribute_col_query and boolean mask
    samples = metadata_table.loc[
    metadata_table.loc[:,attribute_col_query[0]
    ].str.contains(attribute_true_regex)]
    #extracts list of blanks w attribute_col_query and boolean mask
    blanks = metadata_table.loc[
    metadata_table.loc[:,attribute_col_query[0]
    ].str.contains(attribute_false_regex)]
    
    #formats to list using column name stored in sample_col_query
    samples = samples[sample_col_query[0]].to_list()
    blanks = blanks[sample_col_query[0]].to_list()
    
    #put into dictionary
    blank_samples = {"samples" : samples, "blanks" : blanks}
    
    return blank_samples
