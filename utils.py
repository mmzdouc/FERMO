import copy
from dash import html
from datetime import datetime
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re


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

from variables import color_dict


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
        'sample_name' in file {filename} detected. This is forbidden.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'bioactivity'].dtypes == "object": 
        return html.Div(
        f'''
        ❌ Error: Field containing text values (strings) in column 
        'bioactivity' in file {filename} detected.
        This might be also whitespace at the bottom of the column.
        This is not allowed. Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'sample_name'].duplicated().any():
        return html.Div(
        f'''
        ❌ Error: Duplicate values in column 'sample_name'
        in file {filename} detected. This is not allowed.
        Please correct and try again.'''
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

def peaktable_processing(
    uploaded_files_store, 
    dict_params,
    userlib,
    ):
    """FERMO: peaktable processing
    
    Parameters
    ----------
    uploaded_files_store : `dict`
        contains parsed user-provided input data
    dict_params : `dict`
        contains user-provided parameters
    userlib : `dict` or None
        contains matchms.Spectrum objects of optional user-provided lib
    
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

    user_library_name = uploaded_files_store['user_library_name']
    
    
    #convert mgf lists into np arrays
    ms2_dict = dict()
    for ID in mgf:
        ms2_dict[int(ID)] = [
            np.array(mgf[ID][0], dtype=float), 
            np.array(mgf[ID][1], dtype=float),
            ]
    
    #parse metadata file into a dict of sets
    groups = read_from_metadata_table(
        metadata,
        metadata_name,
        )
    
    #collect general sample stats into a dict
    sample_stats = collect_stats_samples(
        peaktable,
        groups,
        bioactivity,
        )
    
    #generates dict with pandas dfs - one per sample
    samples = get_samplespecific_features(
        peaktable, 
        sample_stats,
        dict_params['feature_rel_int_fact'],
        )
    
    #create set of features that are in samples
    detected_features = set_from_sample_tables(samples)

    #generate nested dict with feature information
    feature_dicts = feature_dicts_creation(
        peaktable,
        ms2_dict,
        dict_params['min_nr_ms2'],
        sample_stats,
        detected_features
        )
    
    #determine non-blank/blank of features and assign to feature_dicts
    determine_blank_features(
        samples, 
        feature_dicts, 
        dict_params['column_ret_fact'],
        sample_stats,
        ) 

    #determine non-active/active of features and assign to feature_dicts
    determine_bioactive_features(
        bioactivity, 
        samples,
        feature_dicts, 
        dict_params['bioact_fact'],
        sample_stats,
        bioactivity_name,
        )
    
    #calculate similarity cliques, append info to feature obj and sample stats
    calculate_similarity_cliques(
        feature_dicts,
        sample_stats,
        dict_params['spectral_sim_tol'], 
        dict_params['spec_sim_score_cutoff'], 
        dict_params['max_nr_links_ss'], 
        )
    
    #if spectral library was provided by user, append info to feature objects
    library_search(
        feature_dicts, 
        userlib, 
        dict_params['spectral_sim_tol'],
        dict_params['spec_sim_score_cutoff'],
        dict_params['min_nr_matched_peaks'], 
        )
    
    #search against embedding using ms2query
    # ~ input_folder = os.path.join(
        # ~ os.path.dirname(__file__),
        # ~ 'libraries',)
    # ~ if os.path.exists(input_folder):
        # ~ ms2query_search(
            # ~ feature_dicts, 
            # ~ input_folder)
    print('WARNING: MS2QUERY switched off')
    
    #Appends adducts/isotopes and determines peak collision
    samples = calculate_feature_overlap(
        samples,
        dict_params['mass_dev_ppm'],
        )
    
    #calculates metrics for each feature in each sample
    samples = calculate_metrics(
        samples, 
        feature_dicts,
        ) 
    
    #add pseudo-chromatogram traces for dashboard plotting
    samples = calculate_pseudochrom_traces(samples,)
    
    #filter features in samples after normalized intensity
    for sample in samples:
        samples[sample].sort_values(
            by=['norm_intensity',], 
            inplace=True, 
            ascending=[False]
            )
        samples[sample].reset_index(drop=True, inplace=True)
    
    #prepare output
    input_filenames = {
        'peaktable_name' : uploaded_files_store['peaktable_name'],
        'mgf_name' : uploaded_files_store['mgf_name'],
        'metadata_name' : uploaded_files_store['metadata_name'],
        'bioactivity_name' : uploaded_files_store['bioactivity_name'],
        'user_library_name' : uploaded_files_store['user_library_name'],
    }
    
    #prepare output
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
            FERMO_data['feature_dicts'][ID]['ms2spectrum'] = 'removed_for_JSON_storage'
    
    #loop over sample stats to replace sets with lists
    for entry in FERMO_data['sample_stats']:
        if isinstance(FERMO_data['sample_stats'][entry], set):
            set_to_list = list(FERMO_data['sample_stats'][entry])
            FERMO_data['sample_stats'][entry] = set_to_list
    for group in FERMO_data['sample_stats']['groups_dict']:
        set_to_list = list(FERMO_data['sample_stats']['groups_dict'][group])
        FERMO_data['sample_stats']['groups_dict'][group] = set_to_list

    #Add metadata to session file
    #-time and date
    
    session_metadata = {
        'date' : str(datetime.date(datetime.now())),
        'time' : str(datetime.time(datetime.now())),
        }
    
    #construct storage data structure
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
    
    #Extract a row as series using squeeze()
    samples[selected_sample].loc[
        samples[selected_sample]['feature_ID'] == ID].squeeze(),
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


def calc_diversity_score(sample_stats, samples):
    '''Calculate diversity scores for each sample, return list'''
    list_div_scores = list()
    for sample in samples:
        try:
            list_div_scores.append(round(
                (
                len(
                    set(sample_stats["cliques_per_sample"][sample]).difference(
                        set(sample_stats["set_blank_cliques"])
                        )
                    )
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2))
        except:
            list_div_scores.append(0)
    return list_div_scores

def calc_specificity_score(sample_stats, samples, sample_unique_cliques):
    '''Calculate specificity scores for each sample, return list'''
    list_spec_scores = list()
    for sample in samples:
        try:
            list_spec_scores.append(round(
                (
                (len(sample_unique_cliques[sample]))
                / 
                len(
                    set(sample_stats["cliques_per_sample"][sample]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2))
        except:
            list_spec_scores.append(0)
    return list_spec_scores


def append_scatter_text(
    row,
    fill,
    line,
    width,
    bordercolor,
    feat_dicts
    ):
    '''Create scatter trace with hoverlabel'''
    ID=str(row["feature_ID"])
    
    cosine_ann = "None"
    if feat_dicts[ID]['cosine_annotation']:
        cosine_ann = ''.join([
            feat_dicts[ID]['cosine_annotation_list'][0]['name'],
            ])
    cosine_ann = (cosine_ann[:75] + '...') if len(cosine_ann) > 75 else cosine_ann
    
    ms2query_ann = "None"
    if feat_dicts[ID]['ms2query']:
        ms2query_ann = ''.join([
            feat_dicts[ID]['ms2query_results'][0]['analog_compound_name'],
            ])
    ms2query_ann = (ms2query_ann[:75] + '...') if len(ms2query_ann) > 75 else ms2query_ann
    
    text = (f'Feature ID <b>{row["feature_ID"]}</b>' +
            '<br>' +
            f'<i>m/z</i> <b>{row["precursor_mz"]}</b>' +
            '<br>' +
            f'RT (min) <b>{row["retention_time"]}</b>' +
            '<br>' +
            f'Lib. annot. <b>{cosine_ann}</b>' +
            '<br>' +
            f'MS2Query <b>{ms2query_ann}</b>' +
            '<br>'
            )
    return go.Scatter(
        x=np.array(row['pseudo_chrom_trace'][0]),
        y=np.array(row['pseudo_chrom_trace'][1]),
        fill='toself',
        fillcolor=fill,
        showlegend=False,
        mode="lines",
        line={
            'color' : line,
            'shape' : 'spline',
            'smoothing' : 0.8,
            'width' : width,
            },
        hoverinfo="text", #change to 'skip' if want to suppress
        text=text,
        hoverlabel={
            'bgcolor' : 'white',
            'bordercolor' : bordercolor}
        )
    

def plot_central_chrom(
    sel_sample,
    active_feature_index,
    sample_stats,
    samples,
    subsets,
    feature_dicts,
    ):
    '''Plot central chromatogram'''
    fig = go.Figure()
    fig.update_layout(
        margin = dict(t=0,b=0, r=0),
        height = 300,
        )

    fig.update_xaxes(
        autorange=False,
        visible=True,
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
            ],
        )
    
    fig.update_yaxes(
        autorange=False,
        title_text="Relative Intensity",
        range=[0, 1.05],
        )
    
    for id, row in samples[sel_sample].iterrows():
        if int(row['feature_ID']) in subsets[sel_sample]['blank_ms1']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_yellow'],
                    color_dict['yellow'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_sample_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['purple'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_group_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_remainder']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['green'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_sample_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['purple'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_group_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_remainder']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['cyan'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        else:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['black'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )

    if isinstance(active_feature_index, int):
        fig.add_shape(
            type="rect",
            xref="x", 
            yref="y",
            x0=samples[sel_sample].at[
                active_feature_index, 'rt_start'],
            x1=samples[sel_sample].at[
                active_feature_index, 'rt_stop'], 
            y0=0, 
            y1=(samples[sel_sample].at[
                active_feature_index, 'norm_intensity'] * 1),
            line={
                'color' : color_dict['blue'],
                'width' : 5,
                'dash' : 'dash',}
        )
    
    return fig




def plot_clique_chrom(
    selected_sample,
    active_feature_index,
    active_feature_id,
    sample_stats,
    samples,
    feature_dicts,
    ):
    '''Plot clique chromatogram - overview'''
    fig = go.Figure()
    
    fig.update_layout(
        margin = dict(t=0,b=0,r=0),
        height = 100,
        )
    
    fig.update_yaxes(
        visible=False,
        )
    
    fig.update_xaxes(
        autorange=False,
        title_text="Retention Time (min)",
            range=[
                (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
                (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
                ],
            )

    if isinstance(active_feature_index, int):
        if feature_dicts[str(active_feature_id)]['similarity_clique']:
            for clique_member in feature_dicts[
                str(active_feature_id)]['similarity_clique_list'][0]:
                if clique_member != active_feature_id:
                    try:
                        row = samples[selected_sample].loc[
                            samples[selected_sample]['feature_ID'] 
                            == clique_member].squeeze()
                        fig.add_trace(
                            append_scatter_text(
                                row,
                                color_dict['light_red'],
                                color_dict['red'],
                                3,
                                color_dict['black'],
                                feature_dicts,
                                )
                            )
                    except:
                        pass
        fig.add_trace(
                append_scatter_text(
                    samples[selected_sample].loc[
                        samples[selected_sample]['feature_ID'] 
                        == active_feature_id].squeeze(),
                    color_dict['light_blue'],
                    color_dict['blue'],
                    3,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
    return fig

def plot_mini_chrom(
    selected_sample,
    active_feature_id,
    sample_stats,
    samples,
    feature_dicts,
    ):
    '''Plot mini-chromatogram overview'''
    
    fig = make_subplots(rows=1, cols=1)

    if isinstance(active_feature_id, int):

        try: 
            nr_subplots = len(
                feature_dicts[str(active_feature_id)]['presence_samples'])
        except KeyError:
            nr_subplots = 0
    
        fig = make_subplots(
            rows=nr_subplots, 
            cols=1,
            shared_xaxes=True,
            x_title="Retention Time (min)",
            subplot_titles=[
                x for x in 
                feature_dicts[str(active_feature_id)]['presence_samples']
                ]
            )
        
        fig.update_annotations(
            font_size=12
            )

        fig.update_yaxes(visible=False)
        
        row_counter = 1
        for sample in feature_dicts[str(active_feature_id)]['presence_samples']:
            feature_row = ""
            for id, row in samples[sample].iterrows():
                if row['feature_ID'] == active_feature_id:
                    active_feature_row = copy.deepcopy(row)
                elif row['norm_intensity'] > 0.05:
                    fig.append_trace(append_scatter_text(
                            row,
                            color_dict['light_grey'],
                            color_dict['grey'],
                            2,
                            color_dict['grey'],
                            feature_dicts,
                            ),
                        row=row_counter, 
                        col=1
                        )
            try:
                fig.append_trace(append_scatter_text(
                    active_feature_row,
                    color_dict['blue'],
                    color_dict['black'],
                    2,
                    color_dict['black'],
                    feature_dicts,
                ),
                row=row_counter, 
                col=1
                )
            except TypeError:
                pass

            row_counter = row_counter + 1

    fig.update_xaxes(
        autorange=False,
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
            ],
        )
    
    fig.update_yaxes(
    autorange=False,
    range=[0, 1],
    visible=False,
    )
    
    fig.update_layout(
    margin = dict(r=0,l=0,b=0,t=50),
    )
    
    return fig


def modify_feature_info_df(
    smpl,
    ID,
    index,
    feat_dicts,
    samples,
    ):
    '''Modify feature_info_dataframe for feature info display'''
    #change to str for feature dict querying
    ID = str(ID)
    
    #Intensity per sample
    int_sample = ''.join(
        [str(samples[smpl].at[index, 'intensity']), ' (', smpl,')',]
        )
    
    #best cosine match
    cosine_annotation = None
    if feat_dicts[ID]['cosine_annotation']:
        cosine_annotation = ''.join([
            '(Name: <b>', feat_dicts[ID]['cosine_annotation_list'][0]['name'],
            '</b>;', '<br>', 'Score: ',
            str(feat_dicts[ID]['cosine_annotation_list'][0]['score']), ';',
            '<br>', 'Nr of matched fragments: ',
            str(feat_dicts[ID]['cosine_annotation_list'][0]['nr_matches']),
            ')', ])

    #Best ms2query match
    ann_ms2query = None
    mass_diff_ms2query = None
    class_ms2query = None
    if feat_dicts[ID]['ms2query']:
        ann_ms2query = ''.join([
            'Name: ', feat_dicts[ID]['ms2query_results'][0]['Link'], ';',
            '<br>', 'Score: ', str(round(feat_dicts[ID]['ms2query_results'][0]
                ['ms2query_model_prediction'],3)), ])
        mass_diff_ms2query = ''.join([ 
            'Δ ', str(round(feat_dicts[ID]['ms2query_results'][0]
                ['precursor_mz_difference'],3)),
            ' <i>m/z</i> (',
            str(round(feat_dicts[ID]['ms2query_results'][0]
                ['precursor_mz_analog'],3)), ')',])
        class_ms2query = ''.join([ 
            str(feat_dicts[ID]['ms2query_results'][0]['npc_class_results']),
            ' (NP Classifier);', '<br>',
            str(feat_dicts[ID]['ms2query_results'][0]['cf_subclass']),
            ' (ClassyFire)' ])
    
    fold_diff_list = []
    if feat_dicts[ID]['dict_fold_diff'] is not None:
        for comp in feat_dicts[ID]['sorted_fold_diff']:
            if feat_dicts[ID]['dict_fold_diff'][comp] > 1:
                fold_diff_list.append(''.join([
                    str(feat_dicts[ID]['dict_fold_diff'][comp]),
                    ' (', comp, '),', '<br>',])) 

    combined_list_int = []
    for i in range(len(feat_dicts[ID]['presence_samples'])):
        combined_list_int.append(''.join([
            str(feat_dicts[ID]['intensities_samples'][i]),' (',
            str(feat_dicts[ID]['presence_samples'][i]), '),', '<br>', ]))

    combined_list_bio = []
    if feat_dicts[ID]['bioactivity_associated']:
        for i in range(len(feat_dicts[ID]['presence_samples'])):
            combined_list_bio.append(''.join([
                str(feat_dicts[ID]['bioactivity_samples'][i]), ' (',
                str(feat_dicts[ID]['presence_samples'][i]), '),', '<br>',
                ]))
    else:
        combined_list_bio = [None]
        
    combined_list_adducts = []
    if samples[smpl].at[index, 'putative_adduct_detection']:
        for i in range(len(samples[smpl].at[index, 'putative_adduct_detection'])):
            combined_list_adducts.append(''.join([
                str(samples[smpl].at[index, 'putative_adduct_detection'][i]),
                ',<br>', ]))
    else:
        combined_list_adducts = [None]

    groups_cliques= []
    if feat_dicts[ID]['similarity_clique']:
        for group in feat_dicts[ID]['set_groups_clique']:
            groups_cliques.append(''.join([group, '<br>', ]))
    else:
        groups_cliques = [None]
    
    sim_clique_len = None
    sim_clique_list = None
    if feat_dicts[ID]['similarity_clique']:
        sim_clique_len = len(feat_dicts[ID]['similarity_clique_list'][0])
        sim_clique_list = (', '.join(str(i) for i in 
            feat_dicts[ID]['similarity_clique_list'][0]))

    placeholder = '-----'
    data = [
        ['Feature ID', samples[smpl].at[index, 'feature_ID']],
        ['Precursor <i>m/z</i>', samples[smpl].at[index, 'precursor_mz']],
        ['Retention time (min)', samples[smpl].at[index, 'retention_time']],
        ['Feature intensity (absolute)', int_sample],
        [placeholder, placeholder],
        ['Medium/blank associated', samples[smpl].at[index, 'in_blank']],
        ['Intensity score', round(samples[smpl].at[index, 'rel_intensity_score'],2)], 
        ['Convolutedness score', round(samples[smpl].at[index, 'convolutedness_score'],2)],
        ['Bioactivity score', round(samples[smpl].at[index, 'bioactivity_score'],2)],
        ['Novelty score', round(samples[smpl].at[index, 'novelty_score'],2)],
        [placeholder, placeholder],
        ['User-library: matches', cosine_annotation],
        ['MS2Query: best analog/match', ann_ms2query],
        ['MS2Query: <i>m/z</i> diff. to best analog/match', mass_diff_ms2query],
        ['MS2Query: pred. class of best analog/match', class_ms2query],
        [placeholder, placeholder],
        ['Found in groups', ("".join(f"{i}<br>" for i in feat_dicts[ID]['set_groups']))],
        ['Fold-differences groups', ("".join(str(i) for i in fold_diff_list))],
        ['Intensity per sample', ("".join(str(i) for i in combined_list_int))],
        ['Bioactivity per sample', ("".join(str(i) for i in combined_list_bio))],
        ['Putative adducts', ("".join(str(i) for i in combined_list_adducts))],
        [placeholder, placeholder],
        ['Molecular network ID', feat_dicts[ID]['similarity_clique_number']],
        ['Groups in molecular network', ("".join(str(i) for i in groups_cliques))],
        ['Number of features in MN', sim_clique_len],
        ['IDs of features in MN', sim_clique_list],
    ]
    
    df = pd.DataFrame(data, columns=['Attribute', 'Description'])
    
    return df.to_dict('records')


def empty_feature_info_df():
    '''Return empty dataframe'''
    placeholder = '-----'
    data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (min)', None],
        ['Feature intensity (absolute)', None],
        [placeholder, placeholder],
        ['Medium/blank associated', None],
        ['Intensity score', None], 
        ['Convolutedness score', None],
        ['Bioactivity score', None],
        ['Novelty score', None],
        [placeholder, placeholder],
        ['User-library: matches', None],
        ['MS2Query: best analog/match', None],
        ['MS2Query: <i>m/z</i> diff. to best analog/match', None],
        ['MS2Query: pred. class of best analog/match', None],
        [placeholder, placeholder],
        ['Found in groups', None],
        ['Fold-differences groups', None],
        ['Intensity per sample', None],
        ['Bioactivity per sample', None],
        ['Putative adducts', None],
        [placeholder, placeholder],
        ['Molecular network ID', None],
        ['Groups in molecular network', None],
        ['Number of features in MN', None],
        ['IDs of features in MN', None],
    ]
    
    df = pd.DataFrame(data, columns=['Attribute', 'Description'])
    
    return df.to_dict('records')






def generate_cyto_elements(
    sel_sample,
    active_feature_id,
    feat_dicts,
    sample_stats,
    ):
    '''Generate cytoscape elements.
    
    Notes
    -----
    Creates nested list of cytoscape elements (nodes and edges).
    Using conditional expressions, nodes are colored by applying
    different classes. These classes have stylesheets associated, which 
    are defined in variables.py, and which is 
    called at dashboard startup as "global" variables. 
    
    List comprehension with multiple conditionals:
    do A if condition a
    else do B if condition b
    else do C if condition c
    for i in list
    '''
    ID = str(active_feature_id)

    #tests if currently selected feature is in a similarity clique
    if feat_dicts[ID]['similarity_clique']:
        
        #Create reference lists for consecutive nodes/edges creation
        node_list = list(feat_dicts[ID]['similarity_clique_list'][0])
        edges_list = list(feat_dicts[ID]['similarity_clique_list'][1])
        precursor_list = [feat_dicts[str(i)]['precursor_mz'] for i in node_list]
        id_precursor_dict = {
            node_list[i] : [precursor_list[i],
                            feat_dicts[str(node_list[i])]['feature_ID'],]
            for i in range(len(node_list))
        }
        
        #Creates list of nodes, with each node as a dictionary.
        nodes = [
        
            #first condition: selected, unique to sample
            {
            'data': {
                'id': str(i), 
                'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
            },
            'classes': 'selected_unique_sample',
            }
            if ((id_precursor_dict[i][1] == int(ID))
            and
            (len(feat_dicts[str(i)]['presence_samples']) == 1)
            )
            
            #second condition: selected, unique to group
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'selected_unique_group',
            }
            if ((id_precursor_dict[i][1] == int(ID))
            and
            (len(feat_dicts[str(i)]['set_groups']) == 1)
            and not 
            ('GENERAL' in feat_dicts[str(i)]['set_groups'])
            )
            
            #third condition: selected - RETAIN
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'selected',
            }
            if (id_precursor_dict[i][1] == int(ID))
            
            #fourth condition: in sample, unique to sample
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'sample_unique_sample',
            }
            if (
                (id_precursor_dict[i][1] in 
                    sample_stats['features_per_sample'][sel_sample])
            and
                (sel_sample in feat_dicts[str(i)]['presence_samples'])
            and
                (len(feat_dicts[str(i)]['presence_samples']) == 1)
                )
                
            #fifth condition: in sample, unique to group
            else {
                'data': {
                    'id': str(i), 
                    'label':"".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'sample_unique_group',
            }
            if (
                (id_precursor_dict[i][1] in 
                    sample_stats['features_per_sample'][sel_sample])
            and
                (sel_sample in feat_dicts[str(i)]['presence_samples'])
            and
                (len(feat_dicts[str(i)]['set_groups']) == 1)
            and not 
                ('GENERAL' in feat_dicts[str(i)]['set_groups'])
            )
            
            #sixth condition: in sample, unique to group - RETAIN
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'sample',
            }
            if (
                (id_precursor_dict[i][1] in 
                    sample_stats['features_per_sample'][sel_sample])
            )
            
            #seventh condition: not in sample, unique to the group
            #where it is found
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'default_unique_group',
            }
            if (
                (len(feat_dicts[str(i)]['set_groups']) == 1)
            and
                (feat_dicts[str(i)]['set_groups'] == feat_dicts[ID]['set_groups'])
            and not 
                ('GENERAL' in feat_dicts[str(i)]['set_groups'])
            )
            
            #eight condition: everything else
            else {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'default',
            }
            for i in id_precursor_dict
        ]
        
        #Create list of edges (one dictionary per edge)
        edges = [
            {'data': {
                'source': str(edges_list[i][0]),
                'target': str(edges_list[i][1]),
                'weight': edges_list[i][2],
                'mass_diff' : abs(round(
                    (feat_dicts[str(edges_list[i][0])]['precursor_mz'] -
                    feat_dicts[str(edges_list[i][1])]['precursor_mz']), 3
                    )),
                }
            }
            for i in range(len(edges_list))
        ]
        
        #Concatenate nodes and edges into single list
        elements = nodes + edges

        return elements
    else:
        return []

def add_nodedata(
    data,
    feat_dicts,
    ):
    '''Append node data to df'''
    
    annotation = ''.join([
        (feat_dicts[str(data['id'])]['cosine_annotation_list'][0]['name']
            if feat_dicts[str(data['id'])]['cosine_annotation']
            else 'None '),
        '<b>(user-library)</b>, <br>',
        (feat_dicts[str(data['id'])]['ms2query_results'][0]['analog_compound_name']
            if feat_dicts[str(data['id'])]['ms2query'] else "None"),
        '<b>(MS2Query)</b>',
        ])
        
    combined_list_int = []
    for i in range(len(feat_dicts[str(data['id'])]['presence_samples'])):
        combined_list_int.append(''.join([
            str(feat_dicts[str(data['id'])]['presence_samples'][i]),
            '<br>', ]))

    content = [
        ['Feature ID', data['id']],
        ['Precursor <i>m/z</i>', feat_dicts[str(data['id'])]['precursor_mz']],
        ['Retention time (avg)', feat_dicts[str(data['id'])]['average_retention_time']],
        ['Annotation', annotation],
        ['Detected in samples', ("".join(str(i) for i in combined_list_int))],
    ]
    
    df = pd.DataFrame(content, columns=['Node info', 'Description'])
    
    return df.to_dict('records')


def add_edgedata(data, feat_dicts,):
    '''Append edge data to df'''
    
    content = [
        ['Connected nodes (IDs)', ''.join([data['source'],'--', data['target']])],
        ['Weight of edge', data['weight']],
        ['<i>m/z</i> difference between nodes', data['mass_diff']],
        ]
    df = pd.DataFrame(content, columns=['Edge info', 'Description'])

    return df.to_dict('records')


def export_sel_peaktable(samples, sel_sample):
    '''Return columns from pandas df'''
    return samples[sel_sample].loc[:,[
            'feature_ID',
            'precursor_mz',
            'retention_time',
            'fwhm',
            'intensity',
            'norm_intensity',
            'rt_start',
            'rt_stop',
            'putative_adduct_detection',
            'rel_intensity_score',
            'convolutedness_score',
            'bioactivity_score',
            'novelty_score',
            'in_blank',
            'ms1_only',]]

def export_features(feature_dicts):
    '''From feature dicts, create lists, convert to pandas df'''
    t_feature_ID = []
    t_prec_mz = []
    t_avg_ret_time = []
    t_rt_samples = []
    t_presence_samp = []
    t_int_samples = []
    t_bioact = []
    t_blank = []
    t_sim_cliq_bool = []
    t_sim_cliq_nr = []
    t_cos_ann_list = []
    t_ms2query_list = []
    t_set_groups = []
    t_set_groups_clique = []
    t_dict_fold_diff = []
        
    for ID in feature_dicts:
        t_feature_ID.append(feature_dicts[ID]['feature_ID'])
        t_prec_mz.append(feature_dicts[ID]['precursor_mz'])
        t_avg_ret_time.append(feature_dicts[ID]['average_retention_time'])
        t_rt_samples.append(feature_dicts[ID]['rt_in_samples'])
        t_presence_samp.append(feature_dicts[ID]['presence_samples'])
        t_int_samples.append(feature_dicts[ID]['intensities_samples'])
        t_bioact.append(feature_dicts[ID]['bioactivity_associated'])
        t_blank.append(feature_dicts[ID]['blank_associated'])
        t_sim_cliq_bool.append(feature_dicts[ID]['similarity_clique'])
        t_sim_cliq_nr.append(feature_dicts[ID]['similarity_clique_number'])
        t_cos_ann_list.append(feature_dicts[ID]['cosine_annotation_list'])
        t_ms2query_list.append(feature_dicts[ID]['ms2query_results'])
        t_set_groups.append(feature_dicts[ID]['set_groups'])
        t_set_groups_clique.append(feature_dicts[ID]['set_groups_clique'])
        t_dict_fold_diff.append(feature_dicts[ID]['dict_fold_diff'])
        
    return pd.DataFrame({
        'feature_ID': t_feature_ID,
        'precursor_mz': t_prec_mz,
        'avg_ret_time': t_avg_ret_time,
        'presence_samples': t_presence_samp,
        'ret_time_in_samples': t_rt_samples,
        'intensities_samples': t_int_samples,
        'bioact_assoc': t_bioact,
        'blank_assoc': t_blank,
        'annotation_user_lib': t_cos_ann_list,
        'ms2query_results': t_ms2query_list,
        'groups_assoc': t_set_groups,
        'similarity_clique': t_sim_cliq_bool,
        'similarity_clique_number': t_sim_cliq_nr,
        'similarity_clique_groups': t_set_groups_clique,
        'groups_fold_differences': t_dict_fold_diff,})

##########
#DATA PROCESSING
##########

def session_loading_table(params, files, metadata, version):
    '''Generate table to return upon session loading on loading page'''
    content = [
                ['Date of creation', metadata['date']],
                ['Time of creation', metadata['time']],
                ['FERMO version', version],
                ['-----', '-----'],
                ['Filename: peaktable', files['peaktable_name']],
                ['Filename: MS² data', files['mgf_name']],
                ['Filename: metadata', files['metadata_name']],
                ['Filename: bioactivity', files['bioactivity_name']],
                ['Filename: user-library', files['user_library_name']],
                ['-----', '-----'],
                ['Mass deviation (ppm)', params['mass_dev_ppm']],
                ['Min number of MS² fragments', params['min_nr_ms2']],
                ['Feature relative intensity filter', params['feature_rel_int_fact']],
                ['Bioactivity factor', params['bioact_fact']],
                ['Column retention factor', params['column_ret_fact']],
                ['Spectrum similarity tolerance', params['spectral_sim_tol']],
                ['Spectrum similarity score cutoff', params['spec_sim_score_cutoff']],
                ['Max nr spectrum similarity links', params['max_nr_links_ss']],
                ['Minimum number of matched peaks', params['min_nr_matched_peaks']],
            ]
    return pd.DataFrame(content, columns=['Attribute', 'Description'])


def empty_loading_table():
    '''Generate empty table for loading page'''
    content = [
                ['Date of creation', None],
                ['Time of creation', None],
                ['FERMO version', None],
                ['-----', '-----'],
                ['Filename: peaktable', None],
                ['Filename: MS² data', None],
                ['Filename: metadata', None],
                ['Filename: bioactivity', None],
                ['Filename: user-library', None],
                ['-----', '-----'],
                ['Mass deviation (ppm)', None],
                ['Min number of MS² fragments', None],
                ['Feature relative intensity filter', None],
                ['Bioactivity factor', None],
                ['Column retention factor', None],
                ['Spectrum similarity tolerance', None],
                ['Spectrum similarity score cutoff', None],
                ['Max nr spectrum similarity links', None],
                ['Minimum number of matched peaks', None],
            ]
    return pd.DataFrame(content, columns=['Attribute', 'Description'])
