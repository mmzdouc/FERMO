import pandas as pd
import numpy as np
import matchms
from matchms.Spectrum import Spectrum
import os
from datetime import datetime

from processing.read_from_metadata_table import read_from_metadata_table
from processing.collect_stats_samples import collect_stats_samples
from processing.get_samplespecific_features import get_samplespecific_features
from processing.set_from_sample_tables import set_from_sample_tables
from processing.feature_dicts_creation import feature_dicts_creation
from processing.determine_blank_features import determine_blank_features
from processing.determine_bioactive_features import determine_bioactive_features
from processing.calculate_similarity_cliques import calculate_similarity_cliques
from processing.library_search import library_search
from processing.ms2query_search import ms2query_search
from processing.calculate_feature_overlap import calculate_feature_overlap
from processing.calculate_metrics import calculate_metrics
from processing.calculate_pseudochrom_traces import calculate_pseudochrom_traces

from app_utils.variables import color_dict


def prepare_spectral_library(userlib_dict):
    '''Prepare spectral library using matchMS
    
    Parameters
    ----------
    userlib_dict : `dict`
    
    Returns
    --------
    ref_library : `list`
    '''
    ref_library = list()
    
    for i in userlib_dict:
        mz = np.array(userlib_dict[i][0], dtype=float)
        intensities = np.array(userlib_dict[i][1], dtype=float)
        metadata_ms2 = userlib_dict[i][2]
        
        if not np.all(mz[:-1] <= mz[1:]):
            idx_sorted = np.argsort(mz)
            mz = mz[idx_sorted]
            intensities = intensities[idx_sorted]
        
        ref_library.append(
            Spectrum(
                mz=mz,
                intensities=intensities,
                metadata=metadata_ms2,)
            )
    
    ref_library = [matchms.filtering.add_compound_name(s) 
            for s in ref_library]
    ref_library = [matchms.filtering.normalize_intensities(s) 
        for s in ref_library]
    ref_library = [matchms.filtering.select_by_intensity(s, intensity_from=0.01)
        for s in ref_library]
    ref_library = [matchms.filtering.add_precursor_mz(s)
        for s in ref_library]
    ref_library = [matchms.filtering.require_precursor_mz(s)
        for s in ref_library]

    return ref_library


def write_process_log(log_dict, counter, message):
    '''Writes process log into dict
    
    Parameters
    ----------
    log_dict : `dict`
    counter : `int`
    message : `str`
    
    Returns
    -------
    log_dict : `dict`
    counter : `int`
    
    Notes
    -----
    Prints logging messages to standard output too, good for users 
    to see that something changes; can be later changed
    '''
    print(message)
    
    log_dict[counter] = message
    counter = counter + 1
    return log_dict, counter


def peaktable_processing(
    uploaded_files_store, 
    dict_params,
    ):
    """FERMO: peaktable processing
    
    Parameters
    ----------
    uploaded_files_store : `dict`
        contains parsed user-provided input data
    dict_params : `dict`
        contains user-provided parameters
    
    Returns
    --------
    FERMO_data : `dict`
        contains data to feed into dashboard visualization
    """
    log_dict = dict()
    counter = 0
    
    peaktable_name = uploaded_files_store['peaktable_name']
    peaktable = pd.read_json(uploaded_files_store['peaktable'], orient='split')
    
    mgf_name =  uploaded_files_store['mgf_name']
    mgf = uploaded_files_store['mgf']
    
    ms2_dict = dict()
    for ID in mgf:
        ms2_dict[int(ID)] = [
            np.array(mgf[ID][0], dtype=float), 
            np.array(mgf[ID][1], dtype=float),
            ]
    
    metadata = None
    metadata_name = uploaded_files_store['metadata_name']
    if metadata_name is not None:
        metadata = pd.read_json(uploaded_files_store['metadata'], orient='split')
    
    bioactivity = None
    bioactivity_name = uploaded_files_store['bioactivity_name']
    if bioactivity_name is not None:
        bioactivity = pd.read_json(uploaded_files_store['bioactivity'], orient='split')
        #add bioactivity_original to add also this data to feature objects for later
        #extraction
    
    ref_library = None
    user_library_name = uploaded_files_store['user_library_name']
    userlib_dict = uploaded_files_store['user_library_dict']
    if user_library_name is not None:
        ref_library = prepare_spectral_library(userlib_dict)
    
    ###BEGIN PROCESSING
    
    groups = read_from_metadata_table(
        metadata,
        metadata_name,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            'Completed read_from_metadata_table.py'
            ])
        )

    sample_stats = collect_stats_samples(
        peaktable,
        groups,
        bioactivity,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            'Completed collect_stats_samples.py'
            ])
        )
    
    samples = get_samplespecific_features(
        peaktable, 
        sample_stats,
        dict_params['feature_rel_int_fact'],
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            f'''Completed get_samplespecific_features.py: Relative intensity filter : {dict_params['feature_rel_int_fact']};'''
            ])
        )

    detected_features = set_from_sample_tables(samples)
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            'Completed set_from_sample_tables.py'
            ])
        )

    feature_dicts = feature_dicts_creation(
        peaktable,
        ms2_dict,
        dict_params['min_nr_ms2'],
        sample_stats,
        detected_features
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            f'''Completed feature_dicts_creation.py: Min nr of fragments per MS² spectrum : {dict_params['min_nr_ms2']};'''
            ])
        )
    
    determine_blank_features(
        samples, 
        feature_dicts, 
        dict_params['column_ret_fact'],
        sample_stats,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            f'''Completed determine_blank_features.py: Blank factor : {dict_params['column_ret_fact']};'''
            ])
        )

    determine_bioactive_features(
        bioactivity, 
        samples,
        feature_dicts, 
        dict_params['bioact_fact'],
        sample_stats,
        bioactivity_name,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            f'''Completed determine_bioactive_features.py: QuantData factor : {dict_params['bioact_fact']};'''
            ])
        )
    
    spec_sim_net_alg_used = calculate_similarity_cliques(
        feature_dicts,
        sample_stats,
        dict_params['spectral_sim_tol'], 
        dict_params['spec_sim_score_cutoff'], 
        dict_params['max_nr_links_ss'], 
        dict_params['spec_sim_net_alg'], 
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()), 
            f'''Completed calculate_similarity_cliques.py: Fragment similarity tolerance : {dict_params['spectral_sim_tol']}; Spectrum similarity score cutoff : {dict_params['spec_sim_score_cutoff']}; Max spectral links : {dict_params['max_nr_links_ss']}; Spectral similarity algorithm used: {spec_sim_net_alg_used}'''
            ])
        )

    if user_library_name:
        library_search(
            feature_dicts, 
            ref_library,
            dict_params['spectral_sim_tol'],
            dict_params['spec_sim_score_cutoff'],
            dict_params['min_nr_matched_peaks'], 
            )
        log_dict, counter =  write_process_log(
            log_dict, 
            counter, 
            ': '.join([
                str(datetime.now()), 
                f'''Completed library_search.py: Fragment similarity tolerance : {dict_params['spectral_sim_tol']}; Spectrum similarity score cutoff : {dict_params['spec_sim_score_cutoff']}; Min matched peaks : {dict_params['min_nr_matched_peaks']};'''
                ])
            )
    
    if dict_params['ms2query']:
        input_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'libraries',)
        if os.path.exists(input_folder):
            ms2query_search(
                feature_dicts, 
                input_folder)
            log_dict, counter =  write_process_log(
                log_dict, 
                counter, 
                ': '.join([
                    str(datetime.now()),
                    'Completed ms2query_search.py'
                    ])
                )

    samples = calculate_feature_overlap(
        samples,
        dict_params['mass_dev_ppm'],
        feature_dicts,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()),
            f'''Completed calculate_feature_overlap.py: Fragment similarity tolerance : {dict_params['mass_dev_ppm']};'''
            ])
        )
    
    samples = calculate_metrics(
        samples, 
        feature_dicts,
        sample_stats,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()),
            'Completed calculate_metrics.py'
            ])
        )
    
    samples = calculate_pseudochrom_traces(
        samples,
        )
    log_dict, counter =  write_process_log(
        log_dict, 
        counter, 
        ': '.join([
            str(datetime.now()),
            'Completed calculate_pseudochrom_traces.py'
            ])
        )
    
    for sample in samples:
        samples[sample].sort_values(
            by=['norm_intensity',], 
            inplace=True, 
            ascending=[False]
            )
        samples[sample].reset_index(drop=True, inplace=True)
    
    input_filenames = {
        'peaktable_name' : uploaded_files_store['peaktable_name'],
        'mgf_name' : uploaded_files_store['mgf_name'],
        'metadata_name' : uploaded_files_store['metadata_name'],
        'bioactivity_name' : uploaded_files_store['bioactivity_name'],
        'user_library_name' : uploaded_files_store['user_library_name'],
        }
    
    FERMO_data = {
        'feature_dicts' : feature_dicts,
        'samples' : samples,
        'sample_stats' : sample_stats,
        'params_dict' : dict_params,
        'input_filenames': input_filenames,
        'log_dict' : log_dict,
        }

    return FERMO_data



def make_JSON_serializable(FERMO_data, FERMO_version):
    """Make JSON compatible by removing non-base python data structures
    
    Parameters
    ----------
    FERMO_data : `dict`
    FERMO_version : `str`
    
    Returns
    --------
    storage_JSON_dict : `dict`
    """
    
    #convert pandas dfs to JSON
    samples_JSON = dict()
    for sample in FERMO_data['samples']:
        samples_JSON[sample] = FERMO_data['samples'][sample].to_json(
            orient='split')
    
    #loop over feature_dicts to prepare for storage
    for ID in FERMO_data['feature_dicts']:
        for entry in FERMO_data['feature_dicts'][ID]:
            #convert all sets to lists
            if isinstance(FERMO_data['feature_dicts'][ID][entry], set):
                set_to_list = list(FERMO_data['feature_dicts'][ID][entry])
                FERMO_data['feature_dicts'][ID][entry] = set_to_list
            
            #remove matchms Spectrum object
            FERMO_data['feature_dicts'][ID]['ms2spectrum'] = 'removed'
    
    #loop over sample stats to replace sets with lists
    for entry in FERMO_data['sample_stats']:
        if isinstance(FERMO_data['sample_stats'][entry], set):
            set_to_list = list(FERMO_data['sample_stats'][entry])
            FERMO_data['sample_stats'][entry] = set_to_list
    for group in FERMO_data['sample_stats']['groups_dict']:
        set_to_list = list(FERMO_data['sample_stats']['groups_dict'][group])
        FERMO_data['sample_stats']['groups_dict'][group] = set_to_list
    
    session_metadata = {
        'date' : str(datetime.date(datetime.now())),
        'time' : str(datetime.time(datetime.now())),
        }
    
    storage_JSON_dict = {
        'feature_dicts' : FERMO_data['feature_dicts'],
        'samples_JSON' : samples_JSON,
        'sample_stats' : FERMO_data['sample_stats'],
        'params_dict' : FERMO_data['params_dict'],
        'input_filenames': FERMO_data['input_filenames'],
        'session_metadata': session_metadata,
        'FERMO_version' : FERMO_version,
        'logging_dict' : FERMO_data['log_dict'],
        }
    
    return storage_JSON_dict
