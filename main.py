#python 3.9

#reads peak table and generates features objects to be stored in DB
#$1: peaktable in csv format
#$2: mgf-file
#output: "featureobjects-storage.pickle"

###TO DO###
#feature_object_creation.py: implement hash-function
#introduce argparse module to better request command line args


###IMPORTS - EXTERNAL###

import sys
import os
import pandas as pd

###IMPORTS - INTERNAL###

from importing.load_from_peaktable import load_from_peaktable
from importing.load_from_mgf import load_from_mgf
from importing.load_from_feature_objects import load_from_feature_objects
from exporting.store_feature_objects import store_feature_objects
import feature_object_creation as foc
from misc_funct.samples_listing import samples_listing
from misc_funct.precursor_search import precursor_search

#####


if __name__ == "__main__":
    """Switch: 
    if feature object file (pickled) exists in folder, load it;
    else generate feature object file and save (pickle) it
    """
    feature_objects = ""
    peaktable = load_from_peaktable(sys.argv[1])
    if os.path.isfile("example_data/featureobjects.pickle"):
        feature_objects = load_from_feature_objects(
    "example_data/featureobjects.pickle")
        print("Feature objects loaded.")
    else:
        ms2dict = load_from_mgf(sys.argv[2])
        feature_objects = foc.feature_object_creation(peaktable, ms2dict)
        store_feature_objects(feature_objects, 
        "example_data/featureobjects.pickle")
        print("Feature objects loaded.")
    samples = samples_listing(peaktable)
    precursor_search(feature_objects, 522) #testing

    
