from ms2query.run_ms2query import download_zenodo_files
from ms2query.ms2library import create_library_object_from_one_dir
import os

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
    Directly modifies the feature objects, so no return value.
    '''
    query_spectra = list()
    zenodo_DOIs = {"positive": 6997924, "negative": 7107654}
    
    for i in feature_dicts:
        if (
            feature_dicts[i]['ms2spectrum'] is not None
        # ~ and 
            # ~ not feature_dicts[i]['blank_associated']
        ):
            query_spectra.append(feature_dicts[i]['ms2spectrum'])
    
    try:
        download_zenodo_files(zenodo_DOIs['positive'], 
            ms2query_lib_dir)
        download_successful = True
    except:
        download_successful = False
    
    if not download_successful:
        if not os.path.isdir(ms2query_lib_dir):
            print('WARNING: Could not find MS2Query files in folder \
            "libraries" or download them. Skip MS2Query annotation')
            return
    
    
    ms2library = create_library_object_from_one_dir(
        ms2query_lib_dir)
    

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
