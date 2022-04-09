import pickle

def load_from_pickled_file(filename: str) -> dict[int, "Feature_Object"]:
    """Import a pickled dict containing Feature Objects.
    
    Parameters
    ----------
    filename : `str`
        Valid path to a pickle file.

    Returns
    -------
    loaded_dict : `dict`
        Dict with key:int and value:Feature_Object
    """
    infile = open(filename,'rb')
    loaded_dict = pickle.load(infile)
    infile.close()
    return loaded_dict
