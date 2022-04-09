#python 3.9

#reads peak table and generates features objects to be stored in DB
#$1: peaktable in csv format
#$2: mgf-file
#output: "featureobjects-storage.pickle"


###TO DO###
#feature_object_creation.py: implement hash-function
#introduce argparse module to better request command line args



#Docstrings are formatted following the guidelines on 
#DOCUMENTING PYTHON APIS WITH DOCSTRINGS
#https://developer.lsst.io/python/numpydoc.html#py-docstring-parameter-types




###IMPORTS - EXTERNAL MODULES###

import sys
import os
import pandas as pd

###IMPORTS - INTERNAL FUNCTIONS###

#essential
from importing.read_from_peaktable import read_from_peaktable
from importing.load_from_mgf import load_from_mgf
from importing.load_from_pickled_file import load_from_pickled_file
from exporting.store_as_pickled_file import store_as_pickled_file
from feature_objects.feature_object_creation import feature_object_creation

#auxiliary
from misc_funct.samples_listing import samples_listing
from misc_funct.precursor_search import precursor_search

#####


if __name__ == "__main__":
    """Switch: 
    if feature object file (pickled) exists in folder, load it;
    else generate feature object file and save (pickle) it
    """
    feature_objects = ""
    peaktable = read_from_peaktable(sys.argv[1])
    if os.path.isfile("example_data/featureobjects.pickle"):
        feature_objects = load_from_pickled_file(
        "example_data/featureobjects.pickle")
        print("Feature objects loaded.")
    else:
        ms2spectra_dict = load_from_mgf(sys.argv[2])
        feature_objects = feature_object_creation(peaktable, 
        ms2spectra_dict)
        store_as_pickled_file(feature_objects, 
        "example_data/featureobjects.pickle")
        print("Feature objects stored.")
    #TESTING
    #table ALL
    # ~ print(feature_objects[131].precursor_mz)
    # ~ print(feature_objects[131].presence_sample)
    #table SIMPLE
    # ~ print(feature_objects[422].precursor_mz)
    # ~ print(feature_objects[422].presence_sample)
    
    #rewrite sample_listing completely
    # ~ samples = samples_listing(peaktable)
    precursor_search(feature_objects, 522)
    print(feature_objects[422].fwhm)
    # ~ print(feature_objects[131].ms2spectrum.peaks.intensities)
