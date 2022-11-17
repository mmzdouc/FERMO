import pandas as pd
import numpy as np
import matchms
from matchms.Spectrum import Spectrum
import os
from datetime import datetime


#LOCAL MODULES
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

    peaktable_name = uploaded_files_store['peaktable_name']
    peaktable = pd.read_json(uploaded_files_store['peaktable'], orient='split')
    
    mgf_name =  uploaded_files_store['mgf_name']
    mgf = uploaded_files_store['mgf']

    metadata_name = uploaded_files_store['metadata_name']
    metadata = None
    if metadata_name is not None:
        metadata = pd.read_json(uploaded_files_store['metadata'], orient='split')

    bioactivity_name = uploaded_files_store['bioactivity_name']
    bioactivity = None
    if bioactivity_name is not None:
        bioactivity = pd.read_json(uploaded_files_store['bioactivity'], orient='split')
        #add bioactivity_original to add also this data to feature objects for later
        #extraction

    user_library_name = uploaded_files_store['user_library_name']
    userlib_dict = uploaded_files_store['user_library_dict']
    
    ms2_dict = dict()
    for ID in mgf:
        ms2_dict[int(ID)] = [
            np.array(mgf[ID][0], dtype=float), 
            np.array(mgf[ID][1], dtype=float),
            ]
    
    #prepare user-provided spectral library - convert in matchms objects
    ref_library = list()
    if user_library_name is not None:
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

    print('BEGIN: parse metadata file')
    groups = read_from_metadata_table(
        metadata,
        metadata_name,
        )
    print('DONE')
    
    
    print('BEGIN: collect sample stats')
    sample_stats = collect_stats_samples(
        peaktable,
        groups,
        bioactivity,
        )
    print('DONE')
    
    print('BEGIN: for each sample, collect associated features')
    samples = get_samplespecific_features(
        peaktable, 
        sample_stats,
        dict_params['feature_rel_int_fact'],
        )
    print('DONE')

    print('BEGIN: collect features')
    detected_features = set_from_sample_tables(samples)
    print('DONE')

    print('BEGIN: generate feature dicts')
    feature_dicts = feature_dicts_creation(
        peaktable,
        ms2_dict,
        dict_params['min_nr_ms2'],
        sample_stats,
        detected_features
        )
    print('DONE')
    
    print('BEGIN: determine blank-associatedness of features')
    determine_blank_features(
        samples, 
        feature_dicts, 
        dict_params['column_ret_fact'],
        sample_stats,
        )
    print('DONE')
    

    print('BEGIN: determine bioactivity-associatedness of features')
    determine_bioactive_features(
        bioactivity, 
        samples,
        feature_dicts, 
        dict_params['bioact_fact'],
        sample_stats,
        bioactivity_name,
        )
    print('DONE')
    
    print('BEGIN: calculate spectral similarity network')
    calculate_similarity_cliques(
        feature_dicts,
        sample_stats,
        dict_params['spectral_sim_tol'], 
        dict_params['spec_sim_score_cutoff'], 
        dict_params['max_nr_links_ss'], 
        )
    print('DONE')

    if user_library_name:
        print('BEGIN: compare against spectral library')
        library_search(
            feature_dicts, 
            ref_library,
            dict_params['spectral_sim_tol'],
            dict_params['spec_sim_score_cutoff'],
            dict_params['min_nr_matched_peaks'], 
            )
        print('DONE')

    if dict_params['ms2query']:
        print('BEGIN: MS2Query matching')
        input_folder = os.path.join(
            os.path.dirname(__file__),
            'libraries',)
        if os.path.exists(input_folder):
            ms2query_search(
                feature_dicts, 
                input_folder)
        print('DONE')
    
    print('BEGIN: calculate peak overlap')
    samples = calculate_feature_overlap(
        samples,
        dict_params['mass_dev_ppm'],
        )
    print('DONE')
    
    print('BEGIN: calculate feature scores')
    samples = calculate_metrics(
        samples, 
        feature_dicts,
        )
    print('DONE')
    
    print('BEGIN: calculate pseudo-chromatogram traces')
    samples = calculate_pseudochrom_traces(
        samples,
        )
    print('DONE')
    
    print('BEGIN: sort features in sample for normalized intensity')
    for sample in samples:
        samples[sample].sort_values(
            by=['norm_intensity',], 
            inplace=True, 
            ascending=[False]
            )
        samples[sample].reset_index(drop=True, inplace=True)
    print('DONE')
    
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
        } 
    
    return storage_JSON_dict
