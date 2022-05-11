#!/usr/bin/env python3

###TO DO###
#feature_object_creation.py: implement hash-function


#Docstrings are formatted following the guidelines on 
#DOCUMENTING PYTHON APIS WITH DOCSTRINGS
#https://developer.lsst.io/python/numpydoc.html#py-docstring-parameter-types


###IMPORTS - EXTERNAL MODULES###

import sys
import os
import pandas as pd
import argparse

#keep track of external libraries
#import matchms pyteomics numpy dash


###IMPORTS - INTERNAL FUNCTIONS###

#essential
from importing.read_from_peaktable import read_from_peaktable
from importing.read_from_bioactiv_table import read_from_bioactiv_table
from importing.load_from_mgf import load_from_mgf
from feature_objects.feature_object_creation import feature_object_creation
from metrics_calc.calculate_metrics import calculate_metrics
from metrics_calc.display_metrics import display_metrics
from importing.read_from_metadata_table import read_from_metadata_table
from visualization.dashboard import dashboard
from importing.test_equal_nr_features_ms2 import test_equal_nr_features_ms2

#auxiliary
from misc_funct.precursor_search import precursor_search

###ARGPARSE

def get_arguments():
    """Parsing the arguments"""
    parser = argparse.ArgumentParser(description="",
                                     usage='''
______________________________________________________________________
FERMO: Formulation of mEtrics from Reproducible Metabolomics Objects
______________________________________________________________________
Generic command: python main.py -p [peaktable.csv] -m [ms2.mgf] 
-b [bioactivity.csv] --M [metadata.csv]

Mandatory arguments:
    -p, --peaktable         
                MZmine3 style peaktable in .csv format.
                Peaktable in FULL/ALL mode preferred over SIMPLE mode.
    -m, --mgf         
                MZmine3 style tandem mass spectra-containing .mgf-file.

Optional arguments:
    -b, --bioactivity         
                Bioactivity annotation file in .csv format. 
                Format:
                sample_name,bioactivity
                file1.mzML,inactive
                file2.mzML,active
    -M, --metadata         
                Metadata annotation file in .csv format. Gives info on
                whether a file is a regular sample or blank. 
                Format:
                sample_name,sample_attribute
                file1.mzML,sample
                file2.mzML,blank
    --strictness_min         
                Artificially increases feature width so that feature
                collisions are detected more reliably.
                Default: 0.0 min
    --strictness_ppm         
                Strictness in ppm regarding mass deviation during
                duplicate/adduct calculation.
                Default: 20.0 ppm
    --feature_retain_factor         
                Factor to discard features with less than or equal to
                (1 - filter_retain_factor) relative intensity.
                (e.g. 1: retain all features; 0.95: retain all features
                greater than > 5%% of rel int; 0: discard all features)
                Default: 0.95 (range: 0.1-1)
    --bioactivity_factor         
                Factor to filter for bioactivity-associated feature
                below the minimal inhibitory concentration: how many 
                times must a feature be more intense in the active 
                sample than in the inactive sample.
                Default: 10
    --column_bleed_factor         
                Factor to differentiate sample- and blank-associated
                features: how many times must a feature be more intense
                in a sample than in a blank to be still considered 
                sample-associated (e.g. due to column bleed).
                Default: 10
    ----rel_intensity_threshold
                Sets the threshold on how high the relative intensity
                of a feature must be to be considered interesting
                for isolation (e.g. 0.5: feature must have an intensity
                of greater than or equal to 0.5 relative to the most 
                intense feature in the sample to be considered in 
                the sample scoring).
                Default: 0.5 (range: 0-1)
    --convolutedness_threshold         
                Sets the threshold on how high the convolutedness score
                of a feature must be to be considered interesting
                for isolation (e.g. 0.5: at least 50%% of the feature
                peak must be without peak collision/overlap to 
                be considered in the sample scoring).
                Default: 0.5 (range: 0-1)
    --bioactivity_threshold         
                Sets the threshold on how high the bioactivity score
                of a feature must be to be considered interesting
                for isolation. Currently only a binary value, 
                therefore either 0 (bioactivity ignored) or 1
                (bioactivity considered).
                Default: 1.0 (range: 0 or 1)
    --novelty_threshold        
                PLACEHOLRDER - NOT IMPLEMENTED YET.
                Default: 0.0
    --diversity_threshold         
                PLACEHOLRDER - NOT IMPLEMENTED YET.
                Default: 0.0
    --topn         
                Sets number of topN samples/features to report on.
                Default: 5
_____________________________________________________________
''')
    parser.add_argument("-p", "--peaktable",
                        help=argparse.SUPPRESS, required=True)
    parser.add_argument("-m", "--mgf",
                        help=argparse.SUPPRESS, required=True)
    parser.add_argument("-b", "--bioactivity",
                        help=argparse.SUPPRESS, required=False)
    parser.add_argument("-M", "--metadata",
                        help=argparse.SUPPRESS, required=False)
    parser.add_argument("--strictness_min", help=argparse.SUPPRESS,
                        type=float, default=0.0, required=False)
    parser.add_argument("--strictness_ppm", help=argparse.SUPPRESS,
                        type=float, default=20.0, required=False)
    parser.add_argument("--feature_retain_factor", help=argparse.SUPPRESS,
                        type=float, default=0.95, required=False)
    parser.add_argument("--bioactivity_factor", help=argparse.SUPPRESS,
                        type=int, default=10, required=False)
    parser.add_argument("--column_bleed_factor", help=argparse.SUPPRESS,
                        type=int, default=10, required=False)
    parser.add_argument("--rel_intensity_threshold", help=argparse.SUPPRESS,
                        type=float, default=0.5, required=False)
    parser.add_argument("--convolutedness_threshold", help=argparse.SUPPRESS,
                        type=float, default=0.5, required=False)
    parser.add_argument("--bioactivity_threshold", help=argparse.SUPPRESS,
                        type=float, default=1.0, required=False)
    parser.add_argument("--novelty_threshold", help=argparse.SUPPRESS,
                        type=float, default=0.0, required=False)
    parser.add_argument("--diversity_threshold", help=argparse.SUPPRESS,
                        type=float, default=0.0, required=False)
    parser.add_argument("--topn", help=argparse.SUPPRESS,
                        type=int, default=5, required=False)
    return parser.parse_args()


###COMMAND LINE MODE

if __name__ == "__main__":
        
    #INPUT/OUTPUT PART
    
    #argparse
    args = get_arguments()

    #reads Mzmine3-style peaktable (mandatory)
    peaktable = read_from_peaktable(args.peaktable) 

    #reads mgf-file (mandatory)
    ms2spectra_dict = load_from_mgf(args.mgf)
    
    #tests if each feature has an associated spectrum
    test_equal_nr_features_ms2(peaktable, ms2spectra_dict)
    
    #reads from bioactivity.csv file, if provided 
    bioactivity_samples = read_from_bioactiv_table(args.bioactivity)
    
    #reads from metadata.csv file, if provided 
    attributes_samples = read_from_metadata_table(args.metadata)
    
    #calculates feature objects
    feature_objects = feature_object_creation(peaktable, ms2spectra_dict)
   
    #CALCULATION PART
    #calculates metrics for each sample
    samples = calculate_metrics(
    peaktable, 
    feature_objects, 
    bioactivity_samples, 
    attributes_samples, 
    args) 
    
    #VISUALIZATION PART
    #give an overview of topn scoring samples and features
    topn_samples_features = display_metrics(samples, feature_objects, args.topn)
    
    #initialize dash
    # ~ dashboard(samples, feature_objects, topn_samples_features)
    
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
