import pandas as pd

def read_from_metadata_table(arg: str) -> list:
    """Read a metadata table and scrape names of samples and blanks.
    
    Parameters
    ----------
    arg : `csv`
        Must be in format:
        sample_name,sample_attribute
        sample1.mzML,sample
        sample2.mzML,blank

    Returns
    -------
    blank_samples : `dict`
        Contains a list of samples and a list of blanks(solvent,medium)
        
    Notes
    -------
    In future, can be updated to accept more sample_attributes
    """
    
    #barebone function to test first
    #read peaktable
    #create regex templates for more flexibility
    #filter table
    df = pd.read_csv(arg, sep=',')
    
    
    blank_samples = df
    return blank_samples
