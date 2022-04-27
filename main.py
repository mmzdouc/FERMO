#python 3.9

#reads peak table and generates features objects to be stored in DB
#$1: peaktable in csv format
#$2: mgf-file
#$3: bioactivity of samples in csv format (OPTIONAL)
#$4: sample metadata (solvent blank/medium blank) (OPTIONAL)
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
from importing.read_from_metadata_table import read_from_metadata_table

#auxiliary
from misc_funct.precursor_search import precursor_search

#####


if __name__ == "__main__":
    #INPUT/OUTPUT PART
    feature_objects = ""
    #reads Mzmine3-style peaktable
    peaktable = read_from_peaktable(sys.argv[1])
    
    #tests if bioactivity.csv file was provided
    try:
        bioactivity_samples = read_from_bioactiv_table(sys.argv[3])
    except IndexError:
        print("WARNING: No bioactivity file was specified.")
        bioactivity_samples = False
        
    #tests if metadata.csv file was provided
    try:
        attributes_samples = read_from_metadata_table(sys.argv[4])
    except IndexError:
        print("WARNING: No metadata file was specified.")
        attributes_samples = False
        
        
    #load pickle file if extisting
    if os.path.isfile("example_data/featureobjects.pickle"):
        feature_objects = load_from_pickled_file(
        "example_data/featureobjects.pickle")
        print("Feature objects loaded.")
    else:
        ms2spectra_dict = load_from_mgf(sys.argv[2])
        feature_objects = feature_object_creation(peaktable, 
        ms2spectra_dict)
    
    
    #METRICS CALCULATION PART
    
    #Strictness (in minutes): artificially increases feature width
    #so that more collisions are detected.
    strictness_min = 0.0
    #Strictness in ppm regarding adduct calculation.
    strictness_ppm = 20
    #Factor to discard features with <= (1 - filter_retain_factor)
    #relative intensity (e.g. 1: retain all features; 
    #0.95: retain all features > 5% of rel int; 0:discard all features)
    feature_retain_factor = 0.95
    #Bioactivity-association of features: How many times 
    #must a feature be more intense in the active sample than 
    #in the inactive sample to be still considered bioactivity-associated?
    #Takes into account column bleed, sub-activity concentration.
    bioactivity_factor = 10
    #Sample-association of features: How many times 
    #must a feature be more intense in a sample than in a blank 
    #to be not considered a medium/blank associated feature (i.e. 
    #taking into account column bleed)
    column_bleed_factor = 10
    #Determines how much points/weight is given to convoluteness
    convolutedness_weight = 1.0
    #Determines how much points/weight is given to bioactivity
    bioactivity_weight = 1.0
    #Determines how much points/weight is given to novelty
    novelty_weight = 0
    #Determines how much points/weight is given to diversity
    diversity_weight = 0
    
    
    
    #calculates metrics for each sample
    samples = calculate_metrics(peaktable, feature_objects, 
    bioactivity_samples, attributes_samples, strictness_min, strictness_ppm,
    feature_retain_factor,bioactivity_factor, column_bleed_factor,
    convolutedness_weight, bioactivity_weight, novelty_weight, 
    diversity_weight) 
    
    #give an overview of topn scoring samples and features
    topn = 5
    display_metrics(samples, feature_objects, topn)
    
    
    #stores data for later use
    store_as_pickled_file(feature_objects, 
    "example_data/featureobjects.pickle")
    print("")
    print("Feature objects stored.")
    
    
    #TESTING
    
    #TABLE ALL
    # ~ print(feature_objects[2].precursor_mz)
    # ~ print(feature_objects[131].presence_samples)#
    # ~ print(feature_objects[131].blank_associated)
    #TABLE SIMPLE
    # ~ print(feature_objects[422].precursor_mz)
    # ~ print(feature_objects[422].presence_sample)
    # ~ print(samples["7319_7322.mzML"])
    # ~ precursor_search(feature_objects, 522)
    # ~ print(feature_objects[131].median_fwhm)
    # ~ print(feature_objects[131].retention_time)
    # ~ print(feature_objects[131].feature_max_int)
    # ~ print(feature_objects[131].presence_samples)
    # ~ print(feature_objects[131].intensities_samples)
    # ~ print(feature_objects[131].ms2spectrum.peaks.intensities)
