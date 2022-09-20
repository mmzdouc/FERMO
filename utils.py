from dash import html
import re
import pandas as pd
import os

#LOCAL MODULES
from processing.read_from_metadata_table import read_from_metadata_table
from processing.collect_stats_samples import collect_stats_samples
from processing.feature_dicts_creation import feature_dicts_creation
from processing.get_samplespecific_features import get_samplespecific_features
from processing.determine_blank_features import determine_blank_features
from processing.determine_bioactive_features import determine_bioactive_features
from processing.calculate_similarity_cliques import calculate_similarity_cliques
from processing.library_search import library_search
from processing.ms2query_search import ms2query_search
from processing.calculate_feature_overlap import calculate_feature_overlap
from processing.calculate_metrics import calculate_metrics
from processing.calculate_pseudochrom_traces import calculate_pseudochrom_traces

############
#INPUT TESTING
############

def assert_peaktable_format(peaktable, filename):
    """Test peaktable columns for correct headers (i.e. format)
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    
    if peaktable.filter(regex="^id$").columns.empty:
        return return_error_peaktable_div(filename, 'id')
    elif peaktable.filter(regex="^mz$").columns.empty:
        return return_error_peaktable_div(filename, 'mz')
    elif peaktable.filter(regex="^rt$").columns.empty:
        return return_error_peaktable_div(filename, 'rt')
    elif peaktable.filter(regex="^datafile:").columns.empty:
        return return_error_peaktable_div(filename, 'datafile: ...')
    elif peaktable.filter(regex=":intensity_range:max$").columns.empty:
        return return_error_peaktable_div(filename, '... :intensity_range:max')
    elif peaktable.filter(regex=":feature_state$").columns.empty:
        return return_error_peaktable_div(filename, '... :feature_state')
    elif peaktable.filter(regex=":fwhm$").columns.empty:
        return return_error_peaktable_div(filename, '... :fwhm')
    elif peaktable.filter(regex=":rt$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt')
    elif peaktable.filter(regex=":rt_range:min$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt_range:min')
    elif peaktable.filter(regex=":rt_range:max$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt_range:min')
    else:
        return None


def assert_bioactivity_format(bioactiv_table, filename):
    """Test bioact table for col headers, empty values and trailing spaces
        
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(bioactiv_table.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif bioactiv_table.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "sample_name".'
            )
    elif bioactiv_table.filter(regex="^bioactivity$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "bioactivity".'
            )
    elif bioactiv_table.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'bioactivity'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field in column "bioactivity" of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'sample_name'].astype(str).str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.'''
            )
    elif bioactiv_table.loc[:,'bioactivity'].dtypes == "object": 
        return html.Div(
        f'''
        ❌ Error: Field containing text values (strings) in column 
        'bioactivity' in file {filename} detected.
        This might be also whitespace at the bottom of the column.
        This is forbidden.'''
            )
    else:
        return None


def assert_metadata_format(metadata, filename):
    """Test metadata table for col headers, false values and trailing spaces
    
    Parameters
    ----------
    metadata : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(metadata.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif metadata.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "sample_name".'
            )
    elif metadata.filter(regex="^attribute$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "attribute".'
            )
    elif metadata.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in column 'sample_name' of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^GENERAL$').any():
        return html.Div(
        f'''
        ❌ Error: Signal word "GENERAL" used in file {filename}.
        This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'attribute' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].duplicated().any():
        return html.Div(
        f'''
        ❌ Error: Duplicate values in column 'sample_name'
        in file {filename} detected. This is forbidden.'''
            )
    else:
        return None


def return_error_peaktable_div(filename, header):
    '''Helper function to report where error lay.'''
    return html.Div(
        f'''
        ❌ Error: "{filename}" is missing column(s) titled {header}.
        Is this peaktable in the MZmine3 ALL format? If yes, contact the
        FERMO developers.
        ''')


def assert_mgf_format(ms2_dict):
    """Test mgf file for format and content"""
    assert ms2_dict


############
#PARSING
############


def parse_bioactiv_conc(bioactiv_table, value):
    """Parses bioactivity table and converts values depending on value
        
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    value : `str`
    
    Returns
    --------
    converted_df : `pandas.core.frame.DataFrame`
    
    Notes
    ------
    For reference to 'normalization#, refer to:
    Normalization calculation:
    #Stephan Kolassa 
    #(https://stats.stackexchange.com/users/1352/stephan-kolassa),
    #"scale a number between a range", 
    #URL (version: 2018-04-19): https://stats.stackexchange.com/q/281164
    """
    #scale to 0.1-1.0, lowest becomes highest (0 reserved for inactive)
    if value == 'conc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['bioactivity'] == bioactiv_table['bioactivity'][0]).all():
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
                lambda x: (1 / x))
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df

    #scale to 0.1-1 (for reference, see above)
    elif value == 'perc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['bioactivity'] == bioactiv_table['bioactivity'][0]).all():
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
                lambda x: x)
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df

##########
#DATA PROCESSING
##########

def peaktable_processing(input_file_store, params_dict):
    """FERMO: peaktable processing
    
    Parameters
    ----------
    input_file_store : `dict`
        contains parsed user-provided input data
    params_dict : `dict`
        contains user-provided parameters
    
    Returns
    --------
    FERMO_data : `dict`
        contains data to feed into dashboard visualization
    """
    #parse metadata file into a dict of sets
    groups = read_from_metadata_table(
        input_file_store['metadata'],
        input_file_store['metadata_name'],
        )
    
    #collect general sample stats into a dict
    sample_stats = collect_stats_samples(
        input_file_store['peaktable'],
        groups,
        input_file_store['bioactivity'],
        )
    
    #generate nested dict with feature information
    feature_dicts = feature_dicts_creation(
        input_file_store['peaktable'],
        input_file_store['mgf'],
        params_dict['min_nr_ms2'],
        sample_stats
        )
    
    #generates dict with pandas dfs - one per sample
    samples = get_samplespecific_features(
        input_file_store['peaktable'], 
        sample_stats,
        params_dict['feature_rel_int_fact'],
        )
    
    #determine non-blank/blank of features and assign to feature_dicts
    determine_blank_features(
        samples, 
        feature_dicts, 
        params_dict['column_ret_fact'],
        sample_stats,
        ) 

    #determine non-active/active of features and assign to feature_dicts
    determine_bioactive_features(
        input_file_store['bioactivity'], 
        samples,
        feature_dicts, 
        params_dict['bioact_fact'],
        sample_stats,
        input_file_store['bioactivity_name'],
        )
    
    #calculate similarity cliques, append info to feature obj and sample stats
    calculate_similarity_cliques(
        feature_dicts,
        sample_stats,
        params_dict['spectral_sim_tol'], 
        params_dict['spec_sim_score_cutoff'], 
        params_dict['max_nr_links_ss'], 
        )
    
    #if spectral library was provided by user, append info to feature objects
    library_search(
        feature_dicts, 
        input_file_store['user_library'], 
        params_dict['spectral_sim_tol'],
        params_dict['spec_sim_score_cutoff'],
        params_dict['min_nr_matched_peaks'], 
        )
    
    # ~ #search against embedding using ms2query
    # ~ input_folder = os.path.join(
        # ~ os.path.dirname(__file__),
        # ~ 'libraries',)
    # ~ if os.path.exists(input_folder):
        # ~ ms2query_search(
            # ~ feature_dicts, 
            # ~ input_folder)
    print('DEBUG: Switch on MS2Query')
    
    #Appends adducts/isotopes and determines peak collision
    samples = calculate_feature_overlap(
        samples,
        params_dict['mass_dev_ppm'],
        )
    
    #calculates metrics for each feature in each sample
    samples = calculate_metrics(
        samples, 
        feature_dicts,
        ) 

    samples = calculate_pseudochrom_traces(samples,)
    
    input_filenames = {
        'peaktable_name' : input_file_store['peaktable_name'],
        'mgf_name' : input_file_store['mgf_name'],
        'metadata_name' : input_file_store['metadata_name'],
        'bioactivity_name' : input_file_store['bioactivity_name'],
        'user_library_name' : input_file_store['user_library_name'],
    }
    
    FERMO_data = {
        'feature_dicts' : feature_dicts,
        'samples' : samples,
        'sample_stats' : sample_stats,
        'params_dict' : params_dict,
        'input_filenames': input_filenames,
    }
    
    return FERMO_data

def make_JSON_serializable(FERMO_data):
    """Make JSON compatible by removing non-base python data structures
    
    Parameters
    ----------
    FERMO_data : `dict`
    
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
            FERMO_data['feature_dicts'][ID]['ms2spectrum'] = 'removed_for_JSON_storage'
    
    #loop over sample stats to replace sets with lists
    for entry in FERMO_data['sample_stats']:
        if isinstance(FERMO_data['sample_stats'][entry], set):
            set_to_list = list(FERMO_data['sample_stats'][entry])
            FERMO_data['sample_stats'][entry] = set_to_list
        
    for group in FERMO_data['sample_stats']['groups_dict']:
        set_to_list = list(FERMO_data['sample_stats']['groups_dict'][group])
        FERMO_data['sample_stats']['groups_dict'][group] = set_to_list

    #construct storage data structure
    storage_JSON_dict = {
        'feature_dicts' : FERMO_data['feature_dicts'],
        'samples_JSON' : samples_JSON,
        'sample_stats' : FERMO_data['sample_stats'],
        'params_dict' : FERMO_data['params_dict'],
        'input_filenames': FERMO_data['input_filenames'],
        } 
    
    return storage_JSON_dict

##########
#DASHBOARD
##########


def generate_subsets(
    samples, 
    sample,
    thresholds,
    feature_dicts,
    ):
    """Make subsets of features in sample based on thresholds
    
    Parameters
    ----------
    samples : `dict`
    sample : `str`
    thresholds : `dict`
    feature_dicts : `dict`
    
    Returns
    --------
    `dict`
    
    Notes
    ------
    Additional filters can be added with relative ease:
    Add the filter to the FERMO dashboard
    Connect filter to the callback calculate_feature_score
    Simply add a conditional that adds feature ID to all_select_no_blank
    set. the later operations take care of the right group for plotting
    """
    ###STATS###
    
    #all features per sample
    all_feature_set = set(samples[sample]['feature_ID'])

    #which of these features blank associated
    features_blanks_set = set()
    for feature_ID in all_feature_set:
        if 'BLANK' in feature_dicts[str(feature_ID)]['set_groups']:
            features_blanks_set.add(feature_ID)
    
    #extract features w ms1 only from samples table
    ms1_only_df = samples[sample].loc[
        samples[sample]['ms1_only'] == True
        ]
    ms1_only_set = set(ms1_only_df['feature_ID'])
    
    #combine ms1 and blank features
    blank_ms1_set = features_blanks_set.union(ms1_only_set)
    
    #from all features, filter blank and ms1 features
    all_nonblank_set = all_feature_set.difference(blank_ms1_set)
    
    ###FILTERS###
    
    #filter for numeric thresholds
    filtered_thrsh_df = samples[sample].loc[
        (samples[sample]['rel_intensity_score'] >= thresholds['rel_int']) &
        (samples[sample]['convolutedness_score'] >= thresholds['conv']) &
        (samples[sample]['bioactivity_score'] >= thresholds['bioact']) &
        (samples[sample]['novelty_score'] >= thresholds['nov']) 
        ]
    filtered_thrsh_set = set(filtered_thrsh_df['feature_ID'])

    #subtract ms1 and blanks from features over threshold
    all_select_no_blank = filtered_thrsh_set.difference(blank_ms1_set)
    
    #ADDITIONAL FILTERS: ADD HERE (add feature IDs to all_select_no_blank)
    
    
    #subset of selected sample specific features
    select_sample_spec = set()
    for ID in all_select_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            select_sample_spec.add(ID)
    
    #subset of selected group specific features
    select_group_spec = set()
    for ID in all_select_no_blank.difference(select_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            select_group_spec.add(ID)
    
    #subtract sample spec and group spec features from total
    select_remainder = all_select_no_blank.difference(select_sample_spec)
    select_remainder = select_remainder.difference(select_group_spec)
    
    #non-selected features (subtracted blanks+ms1)
    all_nonsel_no_blank = all_nonblank_set.difference(all_select_no_blank)
    
    #subset of nonselected sample specific features
    nonselect_sample_spec = set()
    for ID in all_nonsel_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            nonselect_sample_spec.add(ID)
    
    #subset of nonselected group specific features
    nonselect_group_spec = set()
    for ID in all_nonsel_no_blank.difference(nonselect_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            nonselect_group_spec.add(ID)
    
    #subtract sample spec and group spec features from total
    nonselect_remainder = all_nonsel_no_blank.difference(nonselect_sample_spec)
    nonselect_remainder = nonselect_remainder.difference(nonselect_group_spec)
    
    return {
        ###GENERAL
        'all_features' : list(all_feature_set),
        'blank_ms1' : list(blank_ms1_set),
        'all_nonblank' : list(all_nonblank_set),
        ###SELECTED
        'all_select_no_blank' : list(all_select_no_blank),
        'select_sample_spec' : list(select_sample_spec),
        'select_group_spec' : list(select_group_spec),
        'select_remainder' : list(select_remainder),
        ###NONSELECTED
        'all_nonsel_no_blank' : list(all_nonsel_no_blank),
        'nonselect_sample_spec' : list(nonselect_sample_spec),
        'nonselect_group_spec' : list(nonselect_group_spec),
        'nonselect_remainder' : list(nonselect_remainder),
        }

