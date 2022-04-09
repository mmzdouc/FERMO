import pickle

def store_as_pickled_file(feature_obj: dict, filename: str) -> "pickle":
    """Store dict as pickle-file.

    Parameters
    ----------
    feature_obj : `dict`
        Dict with key:int and value:Feature_Object
    filename : `str`
        Valid path.
    """
    outfile = open(filename, 'wb')
    pickle.dump(feature_obj, outfile)
    outfile.close()
