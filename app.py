###DASH IMPORTS###
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
from dash import dash_table, ctx, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from statistics import mean

###OTHER EXTERNAL MODULES###

import base64
import diskcache
import io
import json
import matchms
from matchms.Spectrum import Spectrum
import numpy as np
import os
import pandas as pd
from pyteomics import mgf
import sys
import time
import webbrowser

###SUPPRESS TENSORFLOW WARNINGS###
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

###INTERNAL MODULES###
from __version__ import __version__

from app_utils.app_input_testing import (
    assert_peaktable_format,
    div_file_format_error,
    div_successful_load_message,
    div_no_file_loaded,
    test_for_None,
    extract_mgf_for_json_storage,
    div_no_quantbio_format,
    assert_bioactivity_format,
    parse_bioactiv_conc,
    remove_zero_values_df,
    assert_metadata_format,
    prepare_spec_lib_for_json_storage,
    div_session_version_warning,
    empty_loading_table,
    session_loading_table,
    div_session_version_error,
    )

from app_utils.FERMO_peaktable_processing import (
    peaktable_processing,
    make_JSON_serializable
    )

from app_utils.dashboard_functions import (
    generate_subsets,
    calc_diversity_score,
    calc_specificity_score,
    export_features,
    export_sel_peaktable,
    prepare_log_file,
    add_edgedata,
    add_nodedata,
    generate_cyto_elements,
    empty_feature_info_df,
    modify_feature_info_df,
    plot_clique_chrom,
    plot_central_chrom,
    prepare_log_file_filters,
    download_sel_sample_all_features,
    download_sel_sample_sel_features,
    download_all_samples_all_features,
    download_all_samples_selected_features,
    download_all_features,
    download_selected_features,
    plot_sample_chrom,
    )

from app_utils.variables import (
    style_data_table,
    style_data_cond_table,
    style_header_table,
    color_dict,
    )

from pages.pages_header_footer import footer_row, header_row
from pages.pages_landing import landing
from pages.pages_dashboard import dashboard
from pages.pages_processing import processing
# ~ from pages.pages_peakpicking import peakpicking
from pages.pages_loading import loading


#Required for background callbacks
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

##########
#LAYOUT
##########

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title='FERMO',
    )

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server

framework_app = dbc.Container([
        header_row,
        html.Div([
            ##ROUTING
            dcc.Store(id='store_landing'),
            dcc.Store(id='store_processing'),
            dcc.Store(id='store_loading'),
            
            ##PROCESSING
            dcc.Store(id='data_processing_FERMO'),
            dcc.Store(id='processed_data_FERMO'),
            dcc.Store(id='loaded_data_FERMO'),
            
            ##LOCATION - 'BROWSER BAR'
            dcc.Location(id='url', refresh=False), 
            
            ##VARIABLE PAGE CONTENT
            html.Div(id='page_content')
            ]),
        footer_row,
        ], 
    id="bounding_box",
    fluid="True", 
)

app.layout = framework_app

##################################################
####################CALLBACKS#####################
##################################################

#######################
###CALLBACKS ROUTING###
#######################

@callback(
    Output('page_content', 'children'),
    Input('url', 'pathname'),
    )
def app_display_page(pathname):
    '''Routing function on which page to display'''
    if pathname == '/dashboard':
        return dashboard
    elif pathname == '/processing':
        return processing
    elif pathname == '/loading':
        return loading
    else:
        return landing

@callback(
    Output('url', 'pathname'),
    Input('store_landing', 'data'),
    Input('store_processing', 'data'),
    Input('store_loading', 'data'),
    )
def app_return_pathname(
    landing, 
    processing, 
    loading,
    ):
    '''Combine callback input for routing, decision via ctx.triggered_id'''
    if ctx.triggered_id == 'store_landing':
        return landing
    elif ctx.triggered_id == 'store_processing':
        return processing
    elif ctx.triggered_id == 'store_loading':
        return loading

@callback(
    Output('store_landing', 'data'),
    Input('call_processing_button', 'n_clicks'),
    Input('call_loading_button', 'n_clicks'),
    )
def landing_call_pages(
    processing_page, 
    loading_page,
    ):
    '''On button click, redirect to respective page'''
    if not any((
        processing_page, 
        loading_page,
        )):
        raise PreventUpdate
    else:
        if processing_page:
            return '/processing'
        elif loading_page:
            return '/loading'

@callback(
    Output('processing_start_cache', 'children'),
    Output('uploaded_files_store', 'data'),
    Input('call_dashboard_processing', 'n_clicks'),
    State('upload_peaktable_store', 'data'),
    State('upload_mgf_store', 'data'),
    State('upload_bioactiv_store', 'data'),
    State('upload_metadata_store', 'data'),
    State('upload_userlib_store', 'data'),
    )
def processing_start_click(
    start_processing,
    peaktable_store,
    mgf_store,
    bioactiv_store,
    metadata_store,
    userlib_store,
    ):
    '''On button click, test for starting conditions for processing'''
    if not start_processing:
        raise PreventUpdate
    elif (
        (peaktable_store['peaktable_name'] is None) 
    or
        (mgf_store['mgf_name'] is None)
    ):
        raise PreventUpdate
    else:
        dict_uploaded_files = {
            'peaktable' : peaktable_store['peaktable'],
            'peaktable_name' : peaktable_store['peaktable_name'],
            'mgf' : mgf_store['mgf'],
            'mgf_name' : mgf_store['mgf_name'],
            'bioactivity' : bioactiv_store['bioactivity'],
            'bioactivity_original' : bioactiv_store['bioactivity_orig'],
            'bioactivity_name' : bioactiv_store['bioactivity_name'],
            'metadata' : metadata_store['metadata'],
            'metadata_name' : metadata_store['metadata_name'],
            'user_library_dict' : userlib_store['user_library_dict'],
            'user_library_name' : userlib_store['user_library_name'],
        }
        return html.Div('Started processing, please wait ...'
            ), dict_uploaded_files



@callback(
    Output('loading_start_cache', 'children'),
    Input('call_dashboard_loading', 'n_clicks'),
    State('upload_session_storage', 'data'),
)
def loading_start_click(start_loading, session_storage):
    '''On button click, test for starting conditions for loading'''
    if not start_loading:
        raise PreventUpdate
    elif session_storage is None:
        raise PreventUpdate
    else:
        return html.Div('Started processing, please wait ...')



@callback(
    Output('data_processing_FERMO', 'data'),
    Input('processed_data_FERMO', 'data'),
    Input('loaded_data_FERMO', 'data'),
    )
def app_bundle_inputs_dashboard(
    storage,
    loading,
    ):
    '''Bundle inputs, return active option for dashboard visualization'''
    if ctx.triggered_id == 'processed_data_FERMO':
        return storage
    elif ctx.triggered_id == 'loaded_data_FERMO':
        return loading

###############################
###CALLBACKS DATA PROCESSING###
###############################

@callback(
    Output('store_processing', 'data'),
    Output('processed_data_FERMO', 'data'),
    Input('processing_start_cache', 'children'),
    State('out_params_assignment', 'data'),
    State('uploaded_files_store', 'data'),
    background=True,
    manager=background_callback_manager,
    running=[(Output("call_dashboard_processing", "disabled"), True, False),],
)
def app_peaktable_processing(
    signal, 
    dict_params,
    uploaded_files_store
    ):
    '''Call FERMO processing functions, serialize data and store'''
    if signal is None:
        raise PreventUpdate
    else:
        FERMO_data = peaktable_processing(
            uploaded_files_store,
            dict_params,
            )

        storage_JSON_dict = make_JSON_serializable(FERMO_data, __version__)

        return '/dashboard', storage_JSON_dict



@callback(
    Output('store_loading', 'data'),
    Output('loaded_data_FERMO', 'data'),
    Input('loading_start_cache', 'children'),
    State('upload_session_storage', 'data'),
    )
def app_loading_processing(signal, session_storage):
    '''Route loaded data'''
    if signal is None:
        raise PreventUpdate
    else:
        return '/dashboard', session_storage


################################
###CALLBACKS PAGES PROCESSING###
################################

@callback(
    Output('out_params_assignment', 'data'),
    Input('mass_dev_inp', 'value'),
    Input('min_ms2_inpt', 'value'),
    Input('bioact_fact_inp', 'value'),
    Input('column_ret_fact_inp', 'value'),
    Input('spec_sim_tol_inp', 'value'),
    Input('spec_sim_score_cutoff_inp', 'value'),
    Input('spec_sim_max_links_inp', 'value'),
    Input('spec_sim_min_match_inp', 'value'),
    Input('ms2query_toggle_input', 'value'),
    Input('spec_sim_net_alg_toggle_input', 'value'),
    Input('ms2query_blank_annotation', 'value'),
    Input('relative_intensity_filter_range', 'value'),
    Input('ms2query_filter_range', 'value'),
    )
def bundle_params_into_cache(
    mass_dev_ppm, 
    min_nr_ms2, 
    bioact_fact,
    column_ret_fact,
    spectral_sim_tol,
    spec_sim_score_cutoff,
    max_nr_links_ss,
    min_nr_matched_peaks,
    ms2query,
    spec_sim_net_alg,
    ms2query_blank_annotation,
    relative_intensity_filter_range,
    ms2query_filter_range,
    ):
    '''Bundle parameter input values, test for None values'''
    
    if None not in [
        mass_dev_ppm, 
        min_nr_ms2, 
        bioact_fact,
        column_ret_fact,
        spectral_sim_tol,
        spec_sim_score_cutoff,
        max_nr_links_ss,
        min_nr_matched_peaks,
        ms2query,
        spec_sim_net_alg,
        ms2query_blank_annotation,
        relative_intensity_filter_range,
        ms2query_filter_range,
        ]:
        return {
            'mass_dev_ppm' : mass_dev_ppm, 
            'min_nr_ms2' : min_nr_ms2, 
            'bioact_fact' : bioact_fact,
            'column_ret_fact' : column_ret_fact,
            'spectral_sim_tol' : spectral_sim_tol,
            'spec_sim_score_cutoff' : spec_sim_score_cutoff,
            'max_nr_links_ss' : max_nr_links_ss,
            'min_nr_matched_peaks' : min_nr_matched_peaks,
            'ms2query' : ms2query,
            'spec_sim_net_alg' : spec_sim_net_alg,
            'ms2query_blank_annotation' : ms2query_blank_annotation,
            'relative_intensity_filter_range' : relative_intensity_filter_range,
            'ms2query_filter_range' : ms2query_filter_range,
            }
    else:
        raise PreventUpdate

@callback(
    Output('upload-peaktable-output', 'children'),
    Output('upload_peaktable_store', 'data'),
    Input('processing-upload-peaktable', 'contents'),
    State('processing-upload-peaktable', 'filename'),
    )
def upload_peaktable(contents, filename):
    '''Peaktable parsing, format check, storage in json'''
    
    file_store = {'peaktable' : None, 'peaktable_name' : None,}
    
    if contents is None:
        return div_no_file_loaded('peaktable'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            peaktable = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['peaktable'] = None
            file_store['peaktable_name'] = None
            return div_file_format_error(str(filename), '.csv'), file_store
        
        return_assert = assert_peaktable_format(peaktable, filename)
        
        if return_assert is not None:
            file_store['peaktable'] = None
            file_store['peaktable_name'] = None
            return return_assert, file_store
        else:
            peaktable.rename(
                columns={
                    'id' : 'feature_ID',
                    'mz' : 'precursor_mz',
                    'rt' : 'retention_time',
                }, 
                inplace=True,
                )
            file_store['peaktable'] = peaktable.to_json(orient='split')
            file_store['peaktable_name'] = filename
            return div_successful_load_message(str(filename)), file_store

@callback(
    Output('upload-mgf-output', 'children'),
    Output('upload_mgf_store', 'data'),
    Input('processing-upload-mgf', 'contents'),
    State('processing-upload-mgf', 'filename'),
    )
def upload_mgf(contents, filename):
    '''mgf file parsing and format check'''
    
    file_store = {'mgf' : None, 'mgf_name' : None,}

    if contents is None:
        return div_no_file_loaded('.mgf-file'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            ms2dict_store = extract_mgf_for_json_storage(decoded)
            assert ms2dict_store

            file_store['mgf'] = ms2dict_store
            file_store['mgf_name'] = filename
            return div_successful_load_message(str(filename)), file_store
            
        except:
            file_store['mgf'] = None
            file_store['mgf_name'] = None
            return div_file_format_error(str(filename), '.mgf'), file_store

@callback(
    Output('upload-bioactiv-output', 'children'),
    Output('upload_bioactiv_store', 'data'),
    Input('upload-bioactiv', 'contents'),
    State('upload-bioactiv', 'filename'),
    Input('bioact_type', 'value'),
    )
def upload_bioactiv(contents, filename, value):
    '''Quantitative biological data table parsing and format check'''
    
    file_store = {
        'bioactivity' : None,
        'bioactivity_orig' : None,
        'bioactivity_name' : None,
        }
    
    if contents is None:
        return div_no_file_loaded('quantitative biological data'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            bioactiv_table = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['bioactivity'] = None
            file_store['bioactivity_orig'] = None
            file_store['bioactivity_name'] = None
            return div_file_format_error(filename, '.csv'), file_store
        
        if value is None:
            return div_no_quantbio_format(str(value)), file_store
        
        return_assert = assert_bioactivity_format(
            bioactiv_table, 
            str(filename),
            )
        
        if return_assert is not None:
            file_store['bioactivity'] = None
            file_store['bioactivity_orig'] = None
            file_store['bioactivity_name'] = None
            return return_assert, file_store
        else:
            df_no_zeroes = remove_zero_values_df(bioactiv_table)
            converted_df = parse_bioactiv_conc(df_no_zeroes, value)
            file_store['bioactivity'] = converted_df.to_json(orient='split')
            file_store['bioactivity_orig'] = df_no_zeroes.to_json(orient='split')
            file_store['bioactivity_name'] = filename
            return div_successful_load_message(str(filename)), file_store

@callback(
    Output('store_bioact_type', 'children'),
    Input('bioact_type', 'value'),
    )
def store_bioactiv_format(value):
    '''Stores the value of bioactivity data format'''
    return html.Div(value)

@callback(
    Output('upload-metadata-output', 'children'),
    Output('upload_metadata_store', 'data'),
    Input('upload-metadata', 'contents'),
    State('upload-metadata', 'filename'),
    )
def upload_metadata(contents, filename,):
    '''Group metadata table parsing and format check'''
    
    file_store = {'metadata' : None, 'metadata_name' : None,}
    
    if contents is None:
        return div_no_file_loaded('group metadata'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    
        try:
            metadata_table = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['metadata'] = None
            file_store['metadata_name'] = None
            return div_file_format_error(str(filename), '.csv'), file_store
        
        return_assert = assert_metadata_format(metadata_table, filename,)
        if return_assert is not None:
            file_store['metadata'] = None
            file_store['metadata_name'] = None
            return return_assert, file_store
        else:
            file_store['metadata'] = metadata_table.to_json(orient='split')
            file_store['metadata_name'] = filename
            return div_successful_load_message(str(filename)), file_store

@callback(
    Output('upload-userlib-output', 'children'),
    Output('upload_userlib_store', 'data'),
    Input('upload-userlib', 'contents'),
    State('upload-userlib', 'filename'),
    )
def upload_userlib(contents, filename):
    '''mgf file parsing and format check for user-provided spectral lib'''
    
    file_store = {
        'user_library_dict' : None,
        'user_library_name' : None,
        }
    
    if contents is None:
        return div_no_file_loaded('spectral library'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            reflib_dict= prepare_spec_lib_for_json_storage(decoded)
            assert reflib_dict

            file_store['user_library_dict'] = reflib_dict
            file_store['user_library_name'] = filename
            return div_successful_load_message(str(filename)), file_store
        except:
            file_store['user_library_dict'] = None
            file_store['user_library_name'] = None
            return div_file_format_error(str(filename), '.mgf'), file_store


#############################
###CALLBACKS PAGES LOADING###
#############################

@callback(
    Output('upload_session_output', 'children'),
    Output('upload_session_storage', 'data'),
    Output('upload_session_table', 'data'),
    Input('upload-session', 'contents'),
    State('upload-session', 'filename'),
    )
def upload_sessionfile(contents, filename):
    '''JSON session file parsing and storage'''
    
    empty_df = empty_loading_table()
    
    if contents is None:
        return div_no_file_loaded('session file'), None, empty_df.to_dict('records')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            loaded_session_JSON = json.load(
                io.StringIO(decoded.decode('utf-8')))
            version = loaded_session_JSON['FERMO_version']
            version_split = version.split('.')
            major, minor, fix = (
                version_split[0], 
                version_split[1], 
                version_split[2],
                )
        except:
            return (
                div_file_format_error(
                    str(filename),
                    'FERMO session (json)'
                    ), 
                None, 
                empty_df.to_dict('records'),
                )
        
        if major != __version__.split('.')[0]:
            return (
                div_session_version_error(
                    str(filename),
                    version,
                    __version__,
                    ),
                None, 
                empty_df.to_dict('records')
                )
        elif minor != __version__.split('.')[1]:
            return (
                div_session_version_error(
                    str(filename),
                    version,
                    __version__,
                    ),
                None, 
                empty_df.to_dict('records')
                )
        elif fix != __version__.split('.')[2]:
            df = session_loading_table(
                loaded_session_JSON['params_dict'],
                loaded_session_JSON['input_filenames'],
                loaded_session_JSON['session_metadata'],
                loaded_session_JSON['FERMO_version'],
                loaded_session_JSON['logging_dict'],
                )
            return (
                div_session_version_warning(
                    str(filename),
                    version,
                    __version__,
                    ),
                loaded_session_JSON, 
                df.to_dict('records'),
                )
        else:
            df = session_loading_table(
                loaded_session_JSON['params_dict'],
                loaded_session_JSON['input_filenames'],
                loaded_session_JSON['session_metadata'],
                loaded_session_JSON['FERMO_version'],
                loaded_session_JSON['logging_dict'],
                )
            return (
                div_successful_load_message(str(filename)),
                loaded_session_JSON, 
                df.to_dict('records'),
                )

###############################
###CALLBACKS PAGES DASHBOARD###
###############################

@callback(
    Output('selected_viz_toggle_value', 'data'),
    Input('selected_viz_toggle', 'value'),
    )
def store_selected_viz_toggle(
    sel_all_vis,
    ):
    '''Store value toggle of visualization of all or selected features'''
    return {'sel_all_vis' : sel_all_vis}
    

@callback(
    Output('threshold_values', 'data'),
    Input('rel_intensity_threshold', 'value'),
    Input('filter_adduct_isotopes', 'value'),
    Input('bioactivity_threshold', 'value'),
    Input('novelty_threshold', 'value'),
    Input('filter_annotation', 'value'),
    Input('filter_feature_id', 'value'),
    Input('filter_precursor_min', 'value'),
    Input('filter_precursor_max', 'value'),
    Input('filter_spectral_sim_netw', 'value'),
    Input('filter_fold_change', 'value'),
    Input('filter_group', 'value'),
    Input('filter_group_cliques', 'value'),
    Input('peak_overlap_threshold', 'value'),
    )
def read_threshold_values_function(
    rel_intensity_threshold, 
    filter_adduct_isotopes, 
    quant_biological_value, 
    novelty_threshold,
    filter_annotation,
    filter_feature_id,
    filter_precursor_min,
    filter_precursor_max,
    filter_spectral_sim_netw,
    filter_fold_change,
    filter_group,
    filter_group_cliques,
    peak_overlap_threshold,
    ):
    '''Bundle input values'''
    
    if filter_feature_id is None:
        filter_feature_id = ''
    if filter_spectral_sim_netw is None:
        filter_spectral_sim_netw = ''
    if filter_precursor_min is None:
        filter_precursor_min = ''
    if filter_precursor_max is None:
        filter_precursor_max = ''
    if filter_fold_change is None:
        filter_fold_change = ''
    
    if None not in [
        rel_intensity_threshold, 
        filter_adduct_isotopes,
        quant_biological_value, 
        novelty_threshold,
        filter_annotation,
        filter_feature_id,
        filter_precursor_min,
        filter_precursor_max,
        filter_spectral_sim_netw,
        filter_fold_change,
        filter_group,
        filter_group_cliques,
        peak_overlap_threshold,
        ]:
        return {
            'rel_intensity_threshold' : rel_intensity_threshold,
            'filter_adduct_isotopes' : str(filter_adduct_isotopes),
            'quant_biological_value' : quant_biological_value,
            'novelty_threshold' : novelty_threshold,
            'filter_annotation' : filter_annotation,
            'filter_feature_id' : filter_feature_id,
            'filter_precursor_min' : filter_precursor_min,
            'filter_precursor_max' : filter_precursor_max,
            'filter_spectral_sim_netw' : filter_spectral_sim_netw,
            'filter_fold_change' : filter_fold_change,
            'filter_group' : filter_group,
            'filter_group_cliques' : filter_group_cliques,
            'peak_overlap_threshold' : peak_overlap_threshold,
            }
    else:
        raise PreventUpdate

@callback(
        Output('table_sample_names', 'data'),
        Output('samples_subsets', 'data'),
        Output('sample_list', 'data'),
        Input('threshold_values', 'data'),
        Input('data_processing_FERMO', 'data'),
        )
def calculate_feature_score(
        thresholds,
        contents,
        ):
    '''For each sample, create subsets of features and calculate scores'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    samples_subsets = dict()
    for sample in samples:
        samples_subsets[sample] = generate_subsets(
            samples, 
            sample,
            thresholds,
            feature_dicts,)
    
    #how many cliques in this sample are only found in group
    #extract all features per sample (corrected for blanks)
    sample_unique_cliques = dict()
    for sample in samples:
        unique_cliques = set()
        for ID in samples_subsets[sample]['all_nonblank']:
            if (
                (len(feature_dicts[str(ID)]['set_groups_clique']) == 1)
                and
                (sample in feature_dicts[str(ID)]['presence_samples'])
            ):
                unique_cliques.add(
                    feature_dicts[str(ID)]['similarity_clique_number']
                    )
        sample_unique_cliques[sample] = list(unique_cliques)
    
    sample_mean_novelty = dict()
    for sample in samples:
        list_novelty_scores = list()
        for ID in samples_subsets[sample]['all_nonblank']:
            nov_score = feature_dicts[str(ID)]['novelty_score']
            if isinstance(nov_score, int) or isinstance(nov_score, float):
                list_novelty_scores.append(nov_score)
        try:
            sample_mean_novelty[sample] = round(mean(list_novelty_scores),2)
        except:
            sample_mean_novelty[sample] = None
    
    sample_sel_cliques = dict()
    for sample in samples:
        clique_set = set()
        for ID in samples_subsets[sample]['all_select_no_blank']:
            if feature_dicts[str(ID)]['similarity_clique']:
                clique_set.add(feature_dicts[str(ID)]['similarity_clique_number'])
        sample_sel_cliques[sample] = len(clique_set)
        
        
    
    sample_scores = pd.DataFrame({
        'Filename' : [i for i in samples],
        'Group' : [sample_stats['samples_dict'][i] for i in samples],
        'Selected features' : [len(samples_subsets[i][
            'all_select_no_blank']) for i in samples],
        'Selected networks' : [sample_sel_cliques[i] for i in
            sample_sel_cliques],
        'Diversity score' : calc_diversity_score(
            sample_stats, 
            samples),
        'Spec score' : calc_specificity_score(
            sample_stats, 
            samples, 
            sample_unique_cliques),
        'Mean Novelty score' : [sample_mean_novelty[i] for i in sample_mean_novelty],
        'Total' : [len(samples_subsets[i]['all_features']) for i in samples],
        'Non-blank' : [len(samples_subsets[i]['all_nonblank']) for i in samples],
        'Blank & MS1' : [len(samples_subsets[i]['blank_ms1']) for i in samples], 
    })

    sample_scores.sort_values(
        by=[
            'Diversity score',
            'Spec score',
            'Non-blank',
            ], 
        inplace=True, 
        ascending=[False, False, False]
        )
    sample_scores.reset_index(drop=True, inplace=True)
    
    sample_list = sample_scores['Filename'].tolist()
    
    return sample_scores.to_dict('records'), samples_subsets, sample_list



@callback(
        Output('table_general_stats', 'data'),
        Input('samples_subsets', 'data'),
        State('data_processing_FERMO', 'data'),
        )
def plot_general_stats_table(subsets, contents):
    '''Calculate basic statistics, return table'''
    
    sample_stats = contents['sample_stats']
    feature_dicts = contents['feature_dicts']
    samples = sample_stats['samples_list']
    
    set_all_features = set()
    for i in samples:
        set_all_features.update(set(subsets[i]['all_features']))
    
    set_selected_features = set()
    for i in samples:
        set_selected_features.update(set(subsets[i]['all_select_no_blank']))
    
    set_blank_features = set()
    for i in samples:
        set_blank_features.update(set(subsets[i]['blank_ms1']))
    
    set_nonblank_features = set()
    for i in samples:
        set_nonblank_features.update(set(subsets[i]['all_nonblank']))
    
    set_selected_cliques = set()
    for i in samples:
        for ID in set_selected_features:
            if feature_dicts[str(ID)]['similarity_clique']:
                set_selected_cliques.add(
                    feature_dicts[str(ID)]['similarity_clique_number']
                    )
        
    df = pd.DataFrame({
        'Nr of samples' : [len(samples)],
        'Nr of features' : [len(set_all_features)],
        'Selected features' : [len(set_selected_features)],
        'Selected networks' : [len(set_selected_cliques)],
        'Non-blank' : [len(set_nonblank_features)],
        'Blank & MS1' : [len(set_blank_features)],
    })
    
    return df.to_dict('records')




@callback(
    Output('storage_active_sample', 'data'),
    Input('table_sample_names', 'active_cell'),
    Input('table_sample_names', 'data'),
    Input('sample_list', 'data'),
)
def storage_active_sample(data, update_table, sample_list):
    '''Store active cell in dcc.Storage'''
    #Null coalescing assignment: default value if var not assigned
    data = data or {'row' : 0,}
    
    return sample_list[data["row"]]

@callback(
    Output('title_central_chrom', 'children'),
    Input('storage_active_sample', 'data'),
)
def title_central_chrom(selected_sample,):
    return f"""Chromatogram of Sample {selected_sample}"""

@callback(
    Output('chromat_out', 'figure'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_index', 'data'),
    Input('samples_subsets', 'data'),
    Input('selected_viz_toggle_value', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chromatogram(
    selected_sample, 
    active_feature_index,
    samples_subsets,
    selected_viz_toggle_value,
    contents,
    ):
    '''Plot central chromatogram'''
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    feature_dicts = contents['feature_dicts']
    
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    return plot_central_chrom(
        selected_sample,
        active_feature_index,
        sample_stats,
        samples,
        samples_subsets,
        feature_dicts,
        selected_viz_toggle_value['sel_all_vis']
        )

@callback(
    Output('storage_active_feature_index', 'data'),
    Output('storage_active_feature_id', 'data'),
    Input('chromat_out', 'clickData'),
    Input('storage_active_sample', 'data'),
    State('data_processing_FERMO', 'data'),
)
def storage_active_feature(data, selected_sample, contents):
    '''Stores active feature in dcc.Storage'''
    if data is None:
        raise PreventUpdate
    
    if ctx.triggered_id == 'storage_active_sample':
        return None, None
    
    samples_JSON = contents['samples_JSON']
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    data_int = int(data["points"][0]['curveNumber'])
    
    feature_ID = int(samples[selected_sample].loc[data_int, 'feature_ID'])
    
    if data_int <= len(samples[selected_sample]):
        return data_int, feature_ID
    else:
        return 0, None

@callback(
    Output('chromat_clique_out', 'figure'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_index', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chromatogram_clique(
    selected_sample, 
    active_feature_index,
    active_feature_id,
    contents,
    ):
    '''Plot clique chromatogram'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')

    return plot_clique_chrom(
        selected_sample,
        active_feature_index,
        active_feature_id,
        sample_stats,
        samples,
        feature_dicts,)

@callback(
    Output('title_mini_chrom', 'children'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def title_mini_chrom(
    active_feature_id,
    contents,
    ):
    '''Print title of mini chromatograms'''
    feature_dicts = contents['feature_dicts']
    sample_stats = contents['sample_stats']
    
    
    if active_feature_id is None:
        return '''No feature selected - click any feature in the
                chromatogram overview.'''
    
    return f"""Feature {active_feature_id}: Detected Across 
        {len(feature_dicts[str(active_feature_id)]['presence_samples'])} 
        of {len(sample_stats["samples_list"])} Samples"""

@callback(
    Output('mini_chromatograms', 'children'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chrom_overview(
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Plot mini-chromatograms'''
    
    if active_feature_id is None:
        return html.Div()
    
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')

    return plot_sample_chrom(
        selected_sample,
        active_feature_id,
        sample_stats,
        samples,
        feature_dicts,)
    
    
    
    
    

@callback(
    Output('featureinfo_out', 'data'), 
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    Input('storage_active_feature_index', 'data'),
    State('data_processing_FERMO', 'data'),
)
def update_selected_feature(
    selected_sample, 
    active_feature_id,
    active_feature_index,
    contents,
    ):
    '''Return info on active feature'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    if isinstance(active_feature_index, int):
        return modify_feature_info_df(
            selected_sample,
            active_feature_id,
            active_feature_index,
            feature_dicts,
            samples,
            sample_stats,
            )
    else:
        return empty_feature_info_df()

@callback(
    Output('cytoscape', 'elements'),
    Output('cytoscape_error_message', 'children'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def update_cytoscape(
    selected_sample,
    active_feature_id,
    contents,
    ):
    '''Plot spectral similarity network'''
    feature_dicts = contents['feature_dicts']
    sample_stats = contents['sample_stats']
    
    if active_feature_id is None:
        return (
            [], 
            html.Div(
                '''No network selected - click any feature in the
                chromatogram overview.''',
                )
            )
    else:
        network, message = generate_cyto_elements(
            selected_sample,
            active_feature_id,
            feature_dicts,
            sample_stats,
            )
        return (network, message)

@callback(
    Output('click-nodedata-output', 'data'),
    Input('cytoscape', 'tapNodeData'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def displayTapNodeData(
    nodedata, 
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Display node data after cytoscape click'''
    feature_dicts = contents['feature_dicts']
    
    if (
        ctx.triggered_id == 'storage_active_sample'
    or
        ctx.triggered_id == 'storage_active_feature_id'
    ):
        data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (avg)', None],
        ['Annotation', None],
        ['MS2Query class pred', None],
        ['Detected in samples', None],
        ]
        df = pd.DataFrame(data, columns=['Node info', 'Description'])
        return df.to_dict('records')
    
    elif ctx.triggered_id == 'cytoscape':
        return add_nodedata(nodedata, feature_dicts,)

@callback(
    Output('click-edgedata-output', 'data'),
    Input('cytoscape', 'tapEdgeData'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def displayTapEdgeData(
    edgedata, 
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Display edge data after cytoscape click'''
    feature_dicts = contents['feature_dicts']
    
    if (
        ctx.triggered_id == 'storage_active_sample'
    or
        ctx.triggered_id == 'storage_active_feature_id'
    ):
        data = [
        ['Connected nodes (IDs)', None],
        ['Weight of edge', None],
        ['<i>m/z</i> difference between nodes', None],
        ]
        df = pd.DataFrame(data, columns=['Node info', 'Description'])
        return df.to_dict('records')
    
    elif ctx.triggered_id == 'cytoscape':
        return add_edgedata(edgedata, feature_dicts,)



@callback(
    Output("download_feature_export_logging", "data"),
    Output("download_feature_export_button", "data"),
    Input("feature_export_button", "n_clicks"),
    State('storage_active_sample', 'data'),
    State('data_processing_FERMO', 'data'),
    State('dd_export_type', 'value'),
    State('samples_subsets', 'data'),
    State('threshold_values', 'data'),
    )
def export_dd_menu_table(
    n_clicks,
    sel_sample,
    contents,
    option,
    samples_subsets,
    thresholds,
    ):
    '''Export table selected in drop down menu'''
    if n_clicks == 0:
        raise PreventUpdate
    elif option == None:
        raise PreventUpdate
    else:
        if option == 'peak_sel_sam_all_feat':
            return download_sel_sample_all_features(
                sel_sample, 
                contents,
                )
        elif option == 'peak_sel_sam_sel_feat':
            return download_sel_sample_sel_features( 
                sel_sample, 
                contents, 
                samples_subsets, 
                thresholds,
                )
        elif option == 'peak_all_sam_all_feat':
            return download_all_samples_all_features(
                contents
                )
        elif option == 'peak_all_sam_sel_feat':
            return download_all_samples_selected_features(
                contents, 
                samples_subsets, 
                thresholds,
                )
        elif option == 'feature_all':
            return download_all_features(
                contents,
                )
        elif option == 'feature_sel':
            return download_selected_features(
                contents,
                samples_subsets,
                thresholds,
                )
        else:
            raise PreventUpdate

@callback(
    Output("export_session_file", "data"),
    Input("button_export_session", "n_clicks"),
    State('data_processing_FERMO', 'data'),
    )
def export_session_file_json(n_clicks, contents):
    '''Export FERMO data as JSON'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        return dcc.send_string(json.dumps(contents, indent=4), 'FERMO_session.json')

##########
#START APP 
##########


if __name__ == '__main__':
    app.run_server(debug=True) #switch to True for debugging
