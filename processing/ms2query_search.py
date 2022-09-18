from ms2query.run_ms2query import default_library_file_base_names
from ms2query.run_ms2query import download_default_models
from ms2query.ms2library import create_library_object_from_one_dir
import pandas as pd
import numpy as np
import os
import pickle

def ms2query_search(feature_dicts, ms2query_lib_dir):
    '''Compare against embedding using MS2Query
    
    Parameters
    ----------
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    ms2query_lib_dir : `str`
        path to dir containing ms2query libraries
        
    Notes
    -----
    Modifies the feature objects, so no return value.
    Approximately 600,000 compounds to compare against
    '''
    #Download MS2Query library files if not already available
    download_default_models(
        ms2query_lib_dir, 
        default_library_file_base_names(),
        )
    
    #Create subset of features for comparisons:
    #-must have a MS2 spectrum
    #-must not be blank associated
    query_spectra = list()
    for i in feature_dicts:
        if (
            feature_dicts[i]['ms2spectrum'] is not None
        and 
            not feature_dicts[i]['blank_associated']
        ):
            query_spectra.append(feature_dicts[i]['ms2spectrum'])

    #Create a MS2Library object
    ms2library = create_library_object_from_one_dir(
        ms2query_lib_dir, 
        default_library_file_base_names()
    )

    #Run library search and analog search on your files.
    results_ms2query = ms2library.analog_search_return_results_tables(
        query_spectra
    )
    
    #Append results to feature objects 
    for results_table in results_ms2query:
        feature_ID = results_table.query_spectrum.get('id')
        results_info = results_table.export_to_dataframe(
            nr_of_top_spectra = 1
        )
        #add a column that contains a link with inchikey
        results_info['Link'] = ''.join([
            '<b><a href="https://pubchem.ncbi.nlm.nih.gov/#query=',
            results_info.loc[0,'inchikey'],
            '" target="_blank">',
            results_info.loc[0,'analog_compound_name'],
            '</a></b>',
        ])
        
        results_info_dict = results_info.to_dict('records')
        feature_dicts[feature_ID]['ms2query_results'] = results_info_dict
        feature_dicts[feature_ID]['ms2query'] = True










