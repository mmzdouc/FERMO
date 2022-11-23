###DASH IMPORTS###
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
from dash import dash_table, ctx, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

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
    assign_params_to_dict,
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
    plot_mini_chrom,
    plot_clique_chrom,
    plot_central_chrom,
    prepare_log_file_filters
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
            # ~ dcc.Store(id='store_peakpicking'),
            dcc.Store(id='store_loading'),
            
            ##PROCESSING
            dcc.Store(id='data_processing_FERMO'),
            dcc.Store(id='processed_data_FERMO'),
            # ~ dcc.Store(id='peakpicking_data_FERMO'),
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
    # ~ elif pathname == '/peakpicking':
        # ~ return peakpicking
    elif pathname == '/loading':
        return loading
    else:
        return landing

@callback(
    Output('url', 'pathname'),
    Input('store_landing', 'data'),
    Input('store_processing', 'data'),
    # ~ Input('store_peakpicking', 'data'),
    Input('store_loading', 'data'),
    )
def app_return_pathname(
    landing, 
    processing, 
    # ~ peakpicking,
    loading,
    ):
    '''Combine callback input for routing, decision via ctx.triggered_id'''
    if ctx.triggered_id == 'store_landing':
        return landing
    elif ctx.triggered_id == 'store_processing':
        return processing
    # ~ elif ctx.triggered_id == 'store_peakpicking':
        # ~ return peakpicking
    elif ctx.triggered_id == 'store_loading':
        return loading

@callback(
    Output('store_landing', 'data'),
    Input('call_processing_button', 'n_clicks'),
    # ~ Input('call_peakpicking_button', 'n_clicks'),
    Input('call_loading_button', 'n_clicks'),
    )
def landing_call_pages(
    processing_page, 
    # ~ peakpicking_page,
    loading_page,
    ):
    '''On button click, redirect to respective page'''
    if not any((
        processing_page, 
        # ~ peakpicking_page, 
        loading_page,
        )):
        raise PreventUpdate
    else:
        if processing_page:
            return '/processing'
        # ~ elif peakpicking_page:
            # ~ return '/peakpicking'
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
    # ~ Input('peakpicking_data_FERMO', 'data'),
    Input('loaded_data_FERMO', 'data'),
    )
def app_bundle_inputs_dashboard(
    storage,
    # ~ peakpicking,
    loading,
    ):
    '''Bundle inputs, return active option for dashboard visualization'''
    if ctx.triggered_id == 'processed_data_FERMO':
        return storage
    # ~ elif ctx.triggered_id == 'peakpicking_data_FERMO':
        # ~ return peakpicking
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
    Output('params_cache', 'component'),
    Input('mass_dev_inp', 'value'),
    Input('min_ms2_inpt', 'value'),
    Input('feat_int_filt_inp', 'value'),
    Input('bioact_fact_inp', 'value'),
    Input('column_ret_fact_inp', 'value'),
    Input('spec_sim_tol_inp', 'value'),
    Input('spec_sim_score_cutoff_inp', 'value'),
    Input('spec_sim_max_links_inp', 'value'),
    Input('spec_sim_min_match_inp', 'value'),
    Input('ms2query_toggle_input', 'value'),
    Input('spec_sim_net_alg_toggle_input', 'value'),
    )
def bundle_params_into_cache(
    mass_dev, 
    min_ms2, 
    feat_int_filt,
    bioact_fact,
    column_ret_fact,
    spec_sim_tol,
    spec_sim_score_cutoff,
    spec_sim_max_links,
    spec_sim_min_match,
    ms2query,
    spec_sim_net_alg,
    ):
    '''Bundle parameter input values, test for None values'''
    
    return {
        'mass_dev' : test_for_None(mass_dev, 20),
        'min_ms2' : test_for_None(min_ms2, 0),
        'feat_int_filt' : test_for_None(feat_int_filt, 0),
        'bioact_fact' : test_for_None(bioact_fact, 0),
        'column_ret_fact' : test_for_None(column_ret_fact, 0),
        'spec_sim_tol' : test_for_None(spec_sim_tol, 0),
        'spec_sim_score_cutoff' : test_for_None(spec_sim_score_cutoff, 0),
        'spec_sim_max_links' : test_for_None(spec_sim_max_links, 0),
        'spec_sim_min_match' : test_for_None(spec_sim_min_match, 0),
        'ms2query' : ms2query,
        'spec_sim_net_alg' : spec_sim_net_alg,
        }

@callback(
    Output('out_params_assignment', 'data'),
    Input('params_cache', 'component')
    )
def update_params_dict(params_cache):
    '''Assign set params to dict'''
    if params_cache is not None:
        return assign_params_to_dict(params_cache)

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
        except:
            return div_file_format_error(str(filename), 'FERMO session (json)'
                ), None, empty_df.to_dict('records')
        try: 
            params = loaded_session_JSON['params_dict']
            files = loaded_session_JSON['input_filenames']
            metadata = loaded_session_JSON['session_metadata']
            version = loaded_session_JSON['FERMO_version']
            logging = loaded_session_JSON['logging_dict']
        except:
            params = None
            files = None
            metadata = None
            version = None
            logging = None
        
        if (
            (params == None) or 
            (files == None) or 
            (metadata == None) or
            (version == None) or
            (logging == None)
        ):
            return div_file_format_error(str(filename), 'FERMO session (json)'
                ), None, empty_df.to_dict('records')
        elif version != __version__:
            df = session_loading_table(params, files, metadata, version, logging)
            return div_session_version_warning(filename, df, __version__
                ), loaded_session_JSON, df.to_dict('records')
        else:
            df = session_loading_table(params, files, metadata, version, logging)
            return div_successful_load_message(str(filename)
                ), loaded_session_JSON, df.to_dict('records')

###############################
###CALLBACKS PAGES DASHBOARD###
###############################

@callback(
    Output('threshold_values', 'data'),
    Input('rel_intensity_threshold', 'value'),
    Input('convolutedness_threshold', 'value'),
    Input('bioactivity_threshold', 'value'),
    Input('novelty_threshold', 'value'),
    Input('filter_annotation', 'value'),
    Input('filter_feature_id', 'value'),
)
def read_threshold_values_function(
    rel_intensity_threshold, 
    filter_adduct_isotopes, 
    quant_biological_value, 
    novelty_threshold,
    filter_annotation,
    filter_feature_id,
    ):
    '''Bundle input values'''
    
    if None not in [
        rel_intensity_threshold, 
        filter_adduct_isotopes,
        quant_biological_value, 
        novelty_threshold,
        filter_annotation,
        filter_feature_id,
        ]:
        return {
            'rel_intensity_threshold' : rel_intensity_threshold,
            'filter_adduct_isotopes' : str(filter_adduct_isotopes),
            'quant_biological_value' : quant_biological_value,
            'novelty_threshold' : novelty_threshold,
            'filter_annotation' : filter_annotation,
            'filter_feature_id' : filter_feature_id,
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
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    #for each sample, extract rows that corresponds to thresholds
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

    #create dataframe to export to dashboard
    sample_scores = pd.DataFrame({
        'Filename' : [i for i in samples],
        'Group' : [sample_stats['samples_dict'][i] for i in samples],
        'Diversity score' : calc_diversity_score(
            sample_stats, 
            samples),
        'Spec score' : calc_specificity_score(
            sample_stats, 
            samples, 
            sample_unique_cliques),
        'Total' : [len(samples_subsets[i]['all_features']) for i in samples],
        'Non-blank' : [len(samples_subsets[i]['all_nonblank']) for i in samples],
        'Over cutoff' : [len(samples_subsets[i]['all_select_no_blank']) for i in samples],
    })
    
    #Sort df, reset index
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
    State('data_processing_FERMO', 'data'),
)
def plot_chromatogram(
    selected_sample, 
    active_feature_index,
    samples_subsets,
    contents,
    ):
    '''Plot central chromatogram'''
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    feature_dicts = contents['feature_dicts']
    
    #temporarily convert from JSON to pandas DF
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
    #temporarily convert from JSON to pandas DF
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
    
    #temporarily convert from JSON to pandas DF
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
        raise PreventUpdate
    
    return f"""Feature {active_feature_id}: Detected Across 
        {len(feature_dicts[str(active_feature_id)]['presence_samples'])} 
        of {len(sample_stats["samples_list"])} Samples"""

@callback(
    Output('mini_chromatograms', 'figure'),
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
    
    '''Solution to sample name (subplot titles) problem of 
    stacking on top of the chromatograms is simply to 
    plot separate small chromatograms instead of subplots!
    Questionable how scalable but best solution 
    since more adjustable than subplots'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    return plot_mini_chrom(
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
    
    #temporarily convert from JSON to pandas DF
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
        return []
    else:
        return generate_cyto_elements(
            selected_sample,
            active_feature_id,
            feature_dicts,
            sample_stats,
            )

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
    Output("download_peak_table_logging", "data"),
    Output("download_peak_table", "data"),
    Input("button_peak_table", "n_clicks"),
    State('storage_active_sample', 'data'),
    State('data_processing_FERMO', 'data'),
)
def export_sel_sample(n_clicks, sel_sample, contents):
    '''Export peaktable of active sample'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        samples_JSON = contents['samples_JSON']
        param_logging = prepare_log_file(contents)

        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')
        
        df = export_sel_peaktable(samples, sel_sample)
        
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4),
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df.to_csv,
                ''.join([
                    sel_sample.split('.')[0], 
                    '_peaktable_all.csv']),
                )
            )


@callback(
    Output("download_peak_table_selected_features_logging", "data"),
    Output("download_peak_table_selected_features", "data"),
    Input("button_peak_table_selected", "n_clicks"),
    State('storage_active_sample', 'data'),
    State('data_processing_FERMO', 'data'),
    State('samples_subsets', 'data'),
    State('threshold_values', 'data'),
)
def export_sel_sample_sel_features(n_clicks, sel_sample, contents, samples_subsets, thresholds):
    '''Export peaktable of active sample - selected features'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        samples_JSON = contents['samples_JSON']
        param_logging = prepare_log_file_filters(contents, thresholds)

        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')
        
        active_features_set = set()
        for sample in samples_subsets:
            active_features_set.update(
                samples_subsets[sample]['all_select_no_blank']) 

        df = export_sel_peaktable(samples, sel_sample)
        df_new = df[df['feature_ID'].isin(active_features_set)]
        df_new = df_new.reset_index(drop=True)
        
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4),
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df_new.to_csv,
                ''.join([
                    sel_sample.split('.')[0], 
                    '_peaktable_selected.csv']),
                )
            )













@callback(
    Output("download_all_peak_table_logging", "data"),
    Output("download_all_peak_table", "data"),
    Input("button_all_peak_table_all_features", "n_clicks"),
    State('data_processing_FERMO', 'data'),
    )
def export_all_samples_all_features(n_clicks, contents):
    '''Export peaktables of all samples'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        samples_JSON = contents['samples_JSON']
        param_logging = prepare_log_file(contents)

        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')
        
        list_dfs = []
        for sample in samples:
            df = export_sel_peaktable(samples, sample)
            df['sample'] = sample
            list_dfs.append(df)
        df_all = pd.concat(list_dfs)
        
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4),
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df_all.to_csv, 
                'FERMO_all_samples_all_features.csv',
                )
            )

@callback(
    Output("download_selected_all_peak_table_logging", "data"),
    Output("download_selected_all_peak_table", "data"),
    Input("button_all_peak_table_selected_features", "n_clicks"),
    State('data_processing_FERMO', 'data'),
    State('samples_subsets', 'data'),
    State('threshold_values', 'data'),
    )
def export_all_samples_selected_features(n_clicks, contents, samples_subsets, thresholds):
    '''Export selected features in peaktables of all samples'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        samples_JSON = contents['samples_JSON']
        param_logging = prepare_log_file_filters(contents, thresholds)

        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')

        active_features_set = set()
        for sample in samples_subsets:
            active_features_set.update(
                samples_subsets[sample]['all_select_no_blank']) 
        
        mod_dfs = dict()
        for sample in samples:
            mod_dfs[sample] = samples[sample][
                samples[sample]['feature_ID'].isin(active_features_set)]
            mod_dfs[sample] = mod_dfs[sample].reset_index(drop=True)
            
            
        list_dfs = []
        for sample in mod_dfs:
            df = export_sel_peaktable(mod_dfs, sample)
            df['sample'] = sample
            list_dfs.append(df)
        df_all = pd.concat(list_dfs)
        
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4),
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df_all.to_csv, 
                'FERMO_all_samples_selected_features.csv',
                )
            )

@callback(
    Output("download_all_features_table_logging", "data"),
    Output("download_all_features_table", "data"),
    Input("button_all_features_table", "n_clicks"),
    State('data_processing_FERMO', 'data'),
    )
def export_all_features(n_clicks, contents):
    '''Convert feature dicts into df and export'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        feature_dicts = contents['feature_dicts']
        param_logging = prepare_log_file(contents)
        
        df = export_features(feature_dicts)
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4), 
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df.to_csv, 
                'FERMO_all_features.csv',
                )
            )

@callback(
    Output("download_selected_features_table_logging", "data"),
    Output("download_selected_features_table", "data"),
    Input("button_selected_features_table", "n_clicks"),
    State('data_processing_FERMO', 'data'),
    State('samples_subsets', 'data'),
    State('threshold_values', 'data'),
    )
def export_selected_features(n_clicks, contents, samples_subsets, thresholds):
    '''Convert feature dicts into df and export'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        feature_dicts = contents['feature_dicts']
        
        active_features_set = set()
        for sample in samples_subsets:
            active_features_set.update(
                samples_subsets[sample]['all_select_no_blank']) 
        
        active_feature_dict = dict()
        for feature in feature_dicts:
            if int(feature) in active_features_set:
                active_feature_dict[feature] = feature_dicts[feature]
        
        param_logging = prepare_log_file_filters(contents, thresholds)
        df = export_features(active_feature_dict)
        
        return (
            dcc.send_string(
                json.dumps(param_logging, indent=4),
                'processing_audit_trail.json',
                ),
            dcc.send_data_frame(
                df.to_csv, 
                'FERMO_selected_features.csv',
                )
            )







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


# If peakpicking is put back, put this into callbacks processing
# ~ @callback(
    # ~ Output('peakpicking_start_cache', 'children'),
    # ~ Input('call_dashboard_peakpicking', 'n_clicks'),
# ~ )
# ~ def peakpicking_start_click(start_peakpicking):
    # ~ '''On button click, should check for starting conditions for peakpicking
    # ~ STILL NEEDS TO BE IMPLEMENTED '''
    # ~ if not start_peakpicking:
        # ~ raise PreventUpdate
    # ~ #elif clause that tests if input params and data were given -> see call_pages_loading
    # ~ else:
        # ~ return html.Div('Started processing, please wait ...')


# ~ @callback(
    # ~ Output('store_peakpicking', 'data'),
    # ~ Output('peakpicking_data_FERMO', 'data'),
    # ~ Input('peakpicking_start_cache', 'children'),
    #Add parameter and upload inputs here (possibly as State)
    # ~ background=True,
    # ~ manager=background_callback_manager,
    # ~ running=[(Output("call_dashboard_peakpicking", "disabled"), True, False),],
# ~ )
# ~ def app_peakpicking_processing(dashboard_peakpicking): #add data output here
    # ~ '''Call peakpicking and FERMO processing functions, serialize and store data'''
    # ~ if not dashboard_peakpicking:
        # ~ raise PreventUpdate
    # ~ else:
        # ~ return '/dashboard'
