#!/usr/bin/env python3

#reads peak table and generates features objects to be stored in DB
#$1: peaktable in csv format
#$2: mgf-file
#$3: bioactivity of samples in csv format (OPTIONAL)
#$4: sample metadata (solvent blank/medium blank) (OPTIONAL)
#output: "featureobjects-storage.pickle"


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

###ARGPARSE

def get_arguments():
    """Parsing the arguments"""
    parser = argparse.ArgumentParser(description="",
                                     usage='''
______________________________________________________________________
FERMO: Formulation of mEtrics from Reproducible Metabolomics Objects
______________________________________________________________________
Generic command: python3 main.py -p [peaktable.csv] -m [ms2.mgf] 
-b [bioactivity.csv] --metadata [metadata.csv]

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
                Default: 0.95
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
    --convolutedness_weight         
                Determines how much weight is given to convoluteness
                during scoring.
                Default: 1.0
    --bioactivity_weight         
                Determines how much weight is given to bioactivity
                during scoring.
                Default: 1.0
    --novelty_weight         
                Determines how much weight is given to novelty
                during scoring. NOT IMPLEMENTED YET.
                Default: 0
    --diversity_weight         
                Determines how much weight is given to diversity
                during scoring. NOT IMPLEMENTED YET.
                Default: 0
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
    parser.add_argument("--convolutedness_weight", help=argparse.SUPPRESS,
                        type=float, default=1.0, required=False)
    parser.add_argument("--bioactivity_weight", help=argparse.SUPPRESS,
                        type=float, default=1.0, required=False)
    parser.add_argument("--novelty_weight", help=argparse.SUPPRESS,
                        type=float, default=1.0, required=False)
    parser.add_argument("--diversity_weight", help=argparse.SUPPRESS,
                        type=float, default=1.0, required=False)
    parser.add_argument("--topn", help=argparse.SUPPRESS,
                        type=int, default=5, required=False)
    return parser.parse_args()



#ARGPARSE

#add modification to convolutedness score calculation


#Feedback from Mo, Zach, Niek on scoring metrics
#convolutedness: instead of just looking at relative intensities etc,
#it should actually take into account A) how much of the area under the 
#curve is undisturbed; B) how much of the time of the peak is undisturbed
#score = weight * ((area_curve-sum of area under curve of colliding peaks)/area_curve)





###COMMAND LINE MODE

if __name__ == "__main__":
        
    #INPUT/OUTPUT PART
    args = get_arguments()

    #reads Mzmine3-style peaktable (mandatory)
    peaktable = read_from_peaktable(args.peaktable) 

    #reads mgf-file (mandatory)
    ms2spectra_dict = load_from_mgf(args.mgf)
    
    #reads from bioactivity.csv file, if provided 
    bioactivity_samples = read_from_bioactiv_table(args.bioactivity)
    
    #reads from metadata.csv file, if provided 
    attributes_samples = read_from_metadata_table(args.metadata)
    
    #calculates feature objects
    feature_objects = feature_object_creation(peaktable, ms2spectra_dict)
   
    #CALCULATION PART
    #calculates metrics for each sample
    samples = calculate_metrics(
    peaktable, feature_objects, 
    bioactivity_samples, attributes_samples, 
    args.strictness_min, args.strictness_ppm,
    args.feature_retain_factor, args.bioactivity_factor,
    args.column_bleed_factor, args.convolutedness_weight, 
    args.bioactivity_weight, args.novelty_weight,
    args.diversity_weight) 
    
    
    #VISUALIZATION PART
    #give an overview of topn scoring samples and features
    display_metrics(samples, feature_objects, args.topn)
    
    
    
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
