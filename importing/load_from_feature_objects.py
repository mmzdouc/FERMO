import pickle

def load_from_feature_objects(filename):
    """Import function.
    
    Loads dictionary of generated feature objects from pickle file.
    """
    infile = open(filename,'rb')
    loaded_feature_objects = pickle.load(infile)
    infile.close()
    return loaded_feature_objects
