from ms2query.run_ms2query import download_zenodo_files
from ms2query.ms2library import create_library_object_from_one_dir
import os

def get_feature_int_range(
    samples,
    filter_range,
    ):
    '''Return dictionary with feature rel intensities across all samples
    
    Parameters
    ----------
    samples : `dict`
    filter_range : `list`
    
    Returns
    -------
    rel_int : `int`
    '''
    rel_int = dict()
    for sample in samples:
        zip_id_int = zip(
            list(samples[sample]['feature_ID']),
            list(samples[sample]['norm_intensity']),
            )
        
        for i in zip_id_int:
            if i[0] in rel_int:
                rel_int[i[0]].append(round(i[1],4))
            else:
                rel_int[i[0]] = []
                rel_int[i[0]].append(round(i[1],4))
    
    return rel_int

def get_features_inside_filter_range(
    rel_int,
    filter_range,
    ):
    '''Return set of features inside the filter range
    
    Parameters
    ----------
    rel_int : `dict`
    filter_range : `list`
    
    Returns
    -------
    included : `set`
    excluded : `set`
    '''
    included = set()
    excluded = set()
    
    for ID in rel_int:
        if (
        ( max(rel_int[ID]) >= filter_range[0] )
        and
        ( min(rel_int[ID]) <= filter_range[1] ) 
        ):
            included.add(ID)
        else:
            excluded.add(ID)
    
    return included, excluded
    

def ms2query_search(
    feature_dicts,
    ms2query_lib_dir,
    blank_annot,
    filter_range,
    samples,
    sample_stats,
    ):
    '''Compare against embedding using MS2Query
    
    Parameters
    ----------
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    ms2query_lib_dir : `str`
        path to dir containing ms2query libraries
    blank_annot : `bool`
        Indicates if medium components should also be annotated
    filter_range : `list`
        Indicates the relative intensity range of features that 
        should be annotated
    samples : `dict`
    sample_stats : `dict`
    
    Notes
    -----
    Directly modifies the feature objects, so no return value.
    '''
    query_spectra = list()
    zenodo_DOIs = {"positive": 6997924, "negative": 7107654}
    
    rel_int = dict()
    included = set()
    excluded = set()
    feature_subset = set()
    
    if filter_range != [0,1]:
        rel_int = get_feature_int_range(samples, filter_range)
        included, excluded = get_features_inside_filter_range(
            rel_int, 
            filter_range
            )
    
    if excluded:
        for i in excluded:
            sample_stats[
                'ms2query_annotation_excluded_based_on_range_filter'].append(
                {i : rel_int[i]})
        feature_subset = included
    else:
        feature_subset = feature_dicts
    
    if blank_annot:
        for i in feature_subset:
            if feature_dicts[i]['ms2spectrum'] is not None:
                query_spectra.append(feature_dicts[i]['ms2spectrum'])
    else:
        for i in feature_subset:
            if (
                feature_dicts[i]['ms2spectrum'] is not None
            and 
                not feature_dicts[i]['blank_associated']
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
