import pandas as pd
import re

def read_from_peaktable(arg: str) -> pd.DataFrame:
    """Read and test MzMine3-style peaktable, reformat for downstream
    processing.

    Parameters
    ----------
    arg : `csv`
        Reads a .csv-file in MzMine3-format (GNPS Export Module/Submit
        Module -> CSV-export: ALL)

    Returns
    -------
    peaktable : `pandas.core.frame.DataFrame`
    
    Notes
    -------
    Reads two feature tables from MzMine: SIMPLE and FULL/ALL.
    Since SIMPLE only provides limited data, user is warned that 
    this might lead to unexpected behaviour (e.g. fwhm is set to a 
    generic 0.2 min, which is obviously wrong).
    """
    peaktable = pd.read_csv(arg, sep=',')
    
    #test which peaktable was provided: "simple" or "full"
    if peaktable.filter(regex="datafile:").columns.empty:
        print("""
WARNING: Peaktable file provided is in SIMPLE mode.
Some functions might not work as expected.
Feature width at half maximum (fwhm) not provided (set to 0.2 min).
We strongly recommended to provide peaktables in FULL/ALL mode.
"""
        )

    #compiles regex objects
    feature_ID_regex = re.compile(
    '^id$|^row id$|^feature_id$', flags=re.I)
    precursor_mz_regex = re.compile(
    '^mz$|^m/z$|^row mz$|^row m/z$|^precursor_mz$', flags=re.I)
    retention_time_regex = re.compile(
    '^rt$|^row rt$|^row retention time$|^retention_time$', flags=re.I)
    
    #pandas dataframe filtering using regex objects created above
    feature_ID = peaktable.filter(regex=feature_ID_regex).columns
    precursor_mz = peaktable.filter(regex=precursor_mz_regex).columns
    retention_time = peaktable.filter(regex=retention_time_regex).columns
    
    #testing if columns exist
    assert not feature_ID.empty, \
    "Column with feature_ID expected; check peak table"
    assert not precursor_mz.empty, \
    "Column with precursor_mz expected; check peak table"
    assert not retention_time.empty, \
    "Column with retention_time expected; check peak table"
    
    #uniformize column names by renaming
    peaktable.rename(
    columns={feature_ID[0]:"feature_ID", precursor_mz[0]:"precursor_mz",
    retention_time[0]:"retention_time"}, inplace=True)
    return peaktable
