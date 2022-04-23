#python 3.9

#reads peak table and generates features objects to be stored in DB
#$1: peaktable in csv format
#$2: mgf-file
#$3: bioactivity of samples in csv format (OPTIONAL)
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
from importing.read_from_bioactiv_table import read_from_bioactiv_table
from importing.load_from_mgf import load_from_mgf
from importing.load_from_pickled_file import load_from_pickled_file
from exporting.store_as_pickled_file import store_as_pickled_file
from feature_objects.feature_object_creation import feature_object_creation
from metrics_calc.calculate_metrics import calculate_metrics
from metrics_calc.display_metrics import display_metrics

#auxiliary
from misc_funct.precursor_search import precursor_search

#####


if __name__ == "__main__":
    """Switch: 
    if feature object file (pickled) exists in folder, load it;
    else generate feature object file and save (pickle) it
    """
    feature_objects = ""
    peaktable = read_from_peaktable(sys.argv[1])
    #test if bioactivity file was provided
    try:
        bioactivity_samples = read_from_bioactiv_table(sys.argv[3])
    except IndexError:
        print("WARNING: No bioactivity file was specified.")
        bioactivity_samples = False
    #load pickle file if extisting
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
    
    #calculates metrics for each sample
    samples = calculate_metrics(peaktable,
    feature_objects,
    bioactivity_samples, 
    0.0, #strictness in minutes
    20, #strictness in ppm
    0.95, #top 95% of activity/discard bottom 5% of peaks reg rel int
    10) #factor regarding bioactivity-association: how many times 
        #must a feature be more intense in the active sample than 
        #in the inactive sample to be still considered bioactivity-associated
        #Takes into account column bleed, sub-activity concentration
    
    #give an overview
    display_metrics(samples, feature_objects, 5)
    
    
    
    #TESTING
    #TABLE ALL
    # ~ print(feature_objects[2].precursor_mz)
    # ~ print(feature_objects[131].presence_sample)
    #TABLE SIMPLE
    # ~ print(feature_objects[422].precursor_mz)
    # ~ print(feature_objects[422].presence_sample)

    # ~ print(samples["7319_7322.mzML"])
    
    
    
    #apply function complexity metric to samples -> use feature Objects
    #apply function visualization to return of complexity metric
    
    # ~ precursor_search(feature_objects, 522)
    # ~ print(feature_objects[131].median_fwhm)
    # ~ print(feature_objects[131].retention_time)
    # ~ print(feature_objects[131].feature_max_int)
    # ~ print(feature_objects[131].presence_samples)
    # ~ print(feature_objects[131].intensities_samples)
    # ~ print(feature_objects[131].ms2spectrum.peaks.intensities)
