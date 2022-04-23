import pandas as pd

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
    """
    df = pd.read_csv(arg, sep=',')
    inactive = df.loc[df.loc[:,"bioactivity"] == "inactive" ]
    inactive = inactive["sample_name"].to_list()
    active = df.loc[df.loc[:,"bioactivity"] == "active" ]
    active = active["sample_name"].to_list()
    bioactivity_samples = {"active" : active, "inactive" : inactive}
    return bioactivity_samples
