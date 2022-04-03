import pickle

def store_feature_objects(feature_objects, filename):
    """Export-function.
    
    Saves dictionary of generated feature objects in pickle file
    for later use.
    """
    outfile = open(filename, 'wb')
    pickle.dump(feature_objects, outfile)
    outfile.close()
