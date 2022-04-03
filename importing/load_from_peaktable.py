import pandas as pd


def load_from_peaktable(df):
    """Reads MzMine3-style peaktable as dataframe.
    
    This function reads a peaktable and checks for the expected
    format (MzMine2/3).
    
    It further removes the string 'Peak area' from the sample 
    columns for easier retrieval further downstream.
    """
    peaktable = pd.read_csv(df, sep=',')
    
    #tests for correct peaktable format"
    try: 
        peaktable[["row ID", "row m/z", "row retention time"]]
    except KeyError:
        print("KeyError: column names incorrectly formatted.")
        print("'row ID', 'row m/z' or 'row retention time' not found.")
        print("Check format of peak table and try again.")
        return None
    
    #renames sample columns for easier handling
    for old_col_name in peaktable.filter(regex="Peak").columns:
        new_col_name = old_col_name.rsplit(" ")[0]
        peaktable.rename(columns={old_col_name:new_col_name}, inplace=True)
    return peaktable
