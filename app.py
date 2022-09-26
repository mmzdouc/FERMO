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
from  matchms.Spectrum import Spectrum
import numpy as np
import os
import pandas as pd
import pickle
from pyteomics import mgf
import sys
import time

###INTERNAL MODULES###
import utils

from variables import (
    style_data_table,
    style_data_cond_table,
    style_header_table,
    color_dict,
    )

from pages.pages_header_footer import footer_row, header_row
from pages.pages_landing import landing
from pages.pages_dashboard import dashboard
from pages.pages_processing import processing
from pages.pages_mzmine import mzmine
from pages.pages_loading import loading


#Required for background callbacks
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

###VERSIONING###
FERMO_version = 'FERMO_version_0.5'



##########
#LAYOUT
##########

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.GRID],
    suppress_callback_exceptions=True,
    title='FERMO',
    )
server = app.server

framework_app = dbc.Container(
    [
    header_row,
    #content row
    html.Div([
        ###Stores for routing###
        dcc.Store(id='store_landing'),
        dcc.Store(id='store_processing'),
        dcc.Store(id='store_mzmine'),
        dcc.Store(id='store_loading'),
        ###Stores for data processing###
        dcc.Store(id='data_processing_FERMO'),
        dcc.Store(id='processed_data_FERMO'),
        # ~ dcc.Store(id='mzmine_data_FERMO'), #switch on when mzmine is implemented
        dcc.Store(id='loaded_data_FERMO'),
        # represents the browser address bar, invisible
        dcc.Location(id='url', refresh=False), 
        #variable page content rendered in this element
        html.Div(id='page-content')
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
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def app_display_page(pathname):
    '''Routing function on which page to display'''
    #Add:
    #---404
    
    if pathname == '/dashboard':
        return dashboard
    elif pathname == '/processing':
        return processing
    elif pathname == '/mzmine':
        return mzmine
    elif pathname == '/loading':
        return loading
    else:
        return landing

@callback(
    Output('url', 'pathname'),
    Input('store_landing', 'data'),
    Input('store_processing', 'data'),
    Input('store_mzmine', 'data'),
    Input('store_loading', 'data'),
)
def app_return_pathname(landing, processing, mzmine, loading):
    '''Combine callback input for routing. ctx decides which page to return'''
    if ctx.triggered_id == 'store_landing':
        return landing
    elif ctx.triggered_id == 'store_processing':
        return processing
    elif ctx.triggered_id == 'store_mzmine':
        return mzmine
    elif ctx.triggered_id == 'store_loading':
        return loading

@callback(
    Output('store_landing', 'data'),
    Input('call_processing_button', 'n_clicks'),
    Input('call_mzmine_button', 'n_clicks'),
    Input('call_loading_button', 'n_clicks'),
)
def landing_call_pages(
    processing_page, 
    mzmine_page,
    loading_page,):
    '''On button click, redirect to respective page'''
    if not any((processing_page, mzmine_page, loading_page,)):
        raise PreventUpdate
    else:
        if processing_page:
            return '/processing'
        elif mzmine_page:
            return '/mzmine'
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
            'mgf_name' : mgf_store['mgf_name'],
            'bioactivity' : bioactiv_store['bioactivity'],
            'bioactivity_name' : bioactiv_store['bioactivity_name'],
            'metadata' : metadata_store['metadata'],
            'metadata_name' : metadata_store['metadata_name'],
            'user_library_name' : userlib_store['user_library_name'],
        }
        return html.Div('Started processing, please wait ...'), dict_uploaded_files


@callback(
    Output('mzmine_start_cache', 'children'),
    Input('call_dashboard_mzmine', 'n_clicks'),
)
def mzmine_start_click(start_mzmine):
    '''On button click, should check for starting conditions for mzmine
    STILL NEEDS TO BE IMPLEMENTED '''
    if not start_mzmine:
        raise PreventUpdate
    #elif clause that tests if input params and data were given -> see call_pages_loading
    else:
        return html.Div('Started processing, please wait ...')


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
    # ~ Input('mzmine_data_FERMO', 'data'),
    Input('loaded_data_FERMO', 'data'),
    )
def app_bundle_inputs_dashboard(storage, loading): #add mzmine to args
    '''Bundle inputs, return active option for dashboard visualization'''
    if ctx.triggered_id == 'processed_data_FERMO':
        return storage
    # ~ elif ctx.triggered_id == 'mzmine_data_FERMO':
        # ~ return mzmine
    elif ctx.triggered_id == 'loaded_data_FERMO':
        return loading

##########################
###CALLBACKS PROCESSING###
##########################

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
        try:
            ms2_pickle_path = os.path.join(
                os.path.dirname(__file__),
                'assets',
                'FERMO_MS2.pickle',
                )
            ms2spectra = ''
            with open(ms2_pickle_path, 'rb') as handle:
                ms2spectra = pickle.load(handle)
        except:
            print('ERROR: FERMO_MS2.pickle reloading failed.')
        
        userlib = None
        if uploaded_files_store['user_library_name'] is not None:
            try:
                userlib_pickle_path = os.path.join(
                    os.path.dirname(__file__),
                    'assets',
                    'FERMO_USERLIB.pickle',
                    )
                with open(userlib_pickle_path, 'rb') as handle:
                    userlib = pickle.load(handle)
            except:
                print('ERROR: FERMO_USERLIB.pickle reloading failed.')

        FERMO_data = utils.peaktable_processing(
            uploaded_files_store,
            dict_params,
            ms2spectra,
            userlib,
            )
        
        storage_JSON_dict = utils.make_JSON_serializable(FERMO_data, FERMO_version)
        
        return '/dashboard', storage_JSON_dict

@callback(
    Output('store_mzmine', 'data'),
    # ~ Output('mzmine_data_FERMO', 'data'),
    Input('mzmine_start_cache', 'children'),
    #Add parameter and upload inputs here (possibly as State)
    background=True,
    manager=background_callback_manager,
    running=[(Output("call_dashboard_mzmine", "disabled"), True, False),],
)
def app_mzmine_processing(dashboard_mzmine): #add data output here
    '''Call MZmine and FERMO processing functions, serialize and store data'''
    if not dashboard_mzmine:
        raise PreventUpdate
    else:
        #Put all functions for processing here
        #MZmine processing (in try, except ; and if it doesn't work, send 
        #to custom page where it tells user that MZmine failed dze to unknown reasons
        #call peaktable_processing() function
        #call JSON serialization
        #return data
        
        #simulate calculation with sleep -> REMOVE
        time.sleep(3.0)
        
        return '/dashboard'

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
    ):
    '''Bundle parameter input values'''
    return {
    'mass_dev' : mass_dev,
    'min_ms2' : min_ms2,
    'feat_int_filt' : feat_int_filt,
    'bioact_fact' : bioact_fact,
    'column_ret_fact' : column_ret_fact,
    'spec_sim_tol' : spec_sim_tol,
    'spec_sim_score_cutoff' : spec_sim_score_cutoff,
    'spec_sim_max_links' : spec_sim_max_links,
    'spec_sim_min_match' : spec_sim_min_match,
        }

@callback(
    Output('out_params_assignment', 'data'),
    Input('params_cache', 'component')
)
def update_params_dict(params_cache):
    '''Assign set params to dict, with catch for None'''
    
    if params_cache is not None:
        dict_params = dict()
        dict_params['mass_dev_ppm'] = (params_cache['mass_dev']
            if params_cache['mass_dev'] is not None else 20)
        dict_params['min_nr_ms2'] = (params_cache['min_ms2']
            if params_cache['min_ms2'] is not None else 0)
        dict_params['feature_rel_int_fact'] = (params_cache['feat_int_filt']
            if params_cache['feat_int_filt'] is not None else 0)
        dict_params['bioact_fact'] = (params_cache['bioact_fact']
            if params_cache['bioact_fact'] is not None else 0)
        dict_params['column_ret_fact'] = (params_cache['column_ret_fact']
            if params_cache['column_ret_fact'] is not None else 0)
        dict_params['spectral_sim_tol'] = (params_cache['spec_sim_tol']
            if params_cache['spec_sim_tol'] is not None else 0)
        dict_params['spec_sim_score_cutoff'] = (params_cache['spec_sim_score_cutoff']
            if params_cache['spec_sim_score_cutoff'] is not None else 0)
        dict_params['max_nr_links_ss'] = (params_cache['spec_sim_max_links']
            if params_cache['spec_sim_max_links'] is not None else 0)
        dict_params['min_nr_matched_peaks'] = (params_cache['spec_sim_min_match']
            if params_cache['spec_sim_min_match'] is not None else 0)
        return dict_params

@callback(
    Output('upload-peaktable-output', 'children'),
    Output('upload_peaktable_store', 'data'),
    Input('processing-upload-peaktable', 'contents'),
    State('processing-upload-peaktable', 'filename'),
)
def upload_peaktable(contents, filename):
    '''Peaktable parsing and format check'''
    
    file_store = {
        'peaktable' : None,
        'peaktable_name' : None,}
    
    if contents is None:
        return html.Div('No peaktable loaded.'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            peaktable = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['peaktable'] = None
            file_store['peaktable_name'] = None
            return html.Div(
                f'''❌ Error: "{filename}" does not seem to be a file
                 in the .csv-format. Have you selected the right file?'''
                ), file_store
        
        return_assert = utils.assert_peaktable_format(peaktable, filename)
        
        peaktable.rename(
            columns={
                'id' : 'feature_ID',
                'mz' : "precursor_mz",
                'rt' : "retention_time",
                }, inplace=True,)
            
        if return_assert is not None:
            file_store['peaktable'] = None
            file_store['peaktable_name'] = None
            return return_assert, file_store
        else:
            file_store['peaktable'] = peaktable.to_json(orient='split')
            file_store['peaktable_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={'color' : 'green', 'font-weight' : 'bold', }
                ), file_store


@callback(
    Output('upload-mgf-output', 'children'),
    Output('upload_mgf_store', 'data'),
    Input('processing-upload-mgf', 'contents'),
    State('processing-upload-mgf', 'filename'),
)
def upload_mgf(contents, filename):
    '''mgf file parsing and format check'''
    file_store = {'mgf_name' : None,}

    if contents is None:
        return html.Div('No .mgf-file loaded.'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            ms2spectra = dict()
            for spectrum in mgf.read(
                io.StringIO(decoded.decode('utf-8')),
                use_index=False
            ):
                fragments = spectrum.get('m/z array')
                intensities = spectrum.get('intensity array')
                feature_ID = int(spectrum.get('params').get('feature_id'))
                ms2spectra[feature_ID] = [fragments, intensities]
            
            utils.assert_mgf_format(ms2spectra)
            
            ms2_pickle_path = os.path.join(
                os.path.dirname(__file__),
                'assets',
                'FERMO_MS2.pickle',
                )
            with open(ms2_pickle_path, 'wb') as handle:
                pickle.dump(
                    ms2spectra, 
                    handle, 
                    protocol=pickle.HIGHEST_PROTOCOL
                )
            
            file_store['mgf_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={'color' : 'green', 'font-weight' : 'bold', }
                ), file_store
            
        except:
            file_store['mgf_name'] = None
            return html.Div(f'''❌ Error: "{filename}" is not a mgf or
            is falsely formatted. Please check the file and try again.'''
            ), file_store


@callback(
    Output('upload-bioactiv-output', 'children'),
    Output('upload_bioactiv_store', 'data'),
    Input('upload-bioactiv', 'contents'),
    State('upload-bioactiv', 'filename'),
    Input('bioact_type', 'value'),
)
def upload_bioactiv(contents, filename, value):
    '''Bioactivity table parsing and format check'''
    
    file_store = {
        'bioactivity' : None,
        'bioactivity_name' : None,}
    
    if contents is None:
        return html.Div('No bioactivity table loaded.'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            bioactiv_table = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['bioactivity'] = None
            file_store['bioactivity_name'] = None
            return html.Div(f'''❌ Error: "{filename}" does not seem to 
                be a file in the .csv-format. Is this the right file?
                '''), file_store
        
        if value is None:
            return html.Div(f'''❌ Error: Please specify the bioactivity
                table format. Currently, the value is {value}.
                '''), file_store
        
        return_assert = utils.assert_bioactivity_format(
            bioactiv_table, 
            filename,
            )
        
        if return_assert is not None:
            file_store['bioactivity'] = None
            file_store['bioactivity_name'] = None
            return return_assert, file_store
        else:
            converted_df = utils.parse_bioactiv_conc(bioactiv_table, value)
            file_store['bioactivity'] = converted_df.to_json(orient='split')
            file_store['bioactivity_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={'color' : 'green','font-weight' : 'bold',}
                ), file_store

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
    '''Metadata table parsing and format check'''
    
    file_store = {
        'metadata' : None,
        'metadata_name' : None,}
    
    if contents is None:
        return html.Div('No metadata table loaded.'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    
        try:
            metadata_table = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except:
            file_store['metadata'] = None
            file_store['metadata_name'] = None
            return html.Div(f'''❌ Error: "{filename}" does not seem to 
            be a file in the .csv-format. Is this the right file?'''
            ), file_store
        
        return_assert = utils.assert_metadata_format(
            metadata_table, 
            filename,
            )
        
        if return_assert is not None:
            file_store['metadata'] = None
            file_store['metadata_name'] = None
            return return_assert, file_store
        else:
            file_store['metadata'] = metadata_table.to_json(orient='split')
            file_store['metadata_name'] = filename
            return html.Div(f'✅ "{filename}" successfully loaded.',
                style={'color' : 'green', 'font-weight' : 'bold',}
                ), file_store


@callback(
    Output('upload-userlib-output', 'children'),
    Output('upload_userlib_store', 'data'),
    Input('upload-userlib', 'contents'),
    State('upload-userlib', 'filename'),
)
def upload_userlib(contents, filename):
    '''mgf file parsing and format check for user-provided spectral lib'''
    
    file_store = {'user_library_name' : None,}
    
    if contents is None:
        return html.Div('No spectral library loaded.'), file_store
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            ref_library = list()
            for spectrum in mgf.read(
                io.StringIO(decoded.decode('utf-8')),
                use_index=False,
            ):
                mz = spectrum.get('m/z array')
                intensities = spectrum.get('intensity array')
                metadata = spectrum.get('params')
                
                if not np.all(mz[:-1] <= mz[1:]):
                    idx_sorted = np.argsort(mz)
                    mz = mz[idx_sorted]
                    intensities = intensities[idx_sorted]
                
                ref_library.append(
                    Spectrum(
                        mz=mz,
                        intensities=intensities,
                        metadata=metadata,
                        )
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
            
            utils.assert_mgf_format(ref_library)

            userlib_pickle_path = os.path.join(
                os.path.dirname(__file__),
                'assets',
                'FERMO_USERLIB.pickle',
                )
            with open(userlib_pickle_path, 'wb') as handle:
                pickle.dump(
                    ref_library, 
                    handle, 
                    protocol=pickle.HIGHEST_PROTOCOL
                )

            file_store['user_library_name'] = filename
            return html.Div(f'✅ "{filename}" successfully loaded.',
                style={'color' : 'green', 'font-weight' : 'bold',}
                    ), file_store
        except:
            file_store['user_library_name'] = None
            return html.Div(f'''❌ Error: "{filename}" is not a mgf or 
                is erroneously formatted (e.g. 'pepmass' must not be 0.0 or 1.0).
                Please check the file and try again.'''
                ), file_store









#######################
###CALLBACKS LOADING###
#######################

@callback(
    Output('upload_session_output', 'children'),
    Output('upload_session_storage', 'data'),
    Output('upload_session_table', 'data'),
    Input('upload-session', 'contents'),
    State('upload-session', 'filename'),
)
def upload_sessionfile(contents, filename):
    '''JSON session file parsing and storage'''
    
    if contents is None:
        return html.Div('No session file loaded.'), None, None
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            loaded_session_JSON = json.load(
                io.StringIO(decoded.decode('utf-8')))
        except:
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a FERMO
                session file in JSON format.
                '''), None, None
        try: 
            params = loaded_session_JSON['params_dict']
            files = loaded_session_JSON['input_filenames']
            metadata = loaded_session_JSON['session_metadata']
            version = loaded_session_JSON['FERMO_version']
        except:
            params = None
            files = None
            metadata = None
            version = None
        
        if (
            (params == None) or 
            (files == None) or 
            (metadata == None) or
            (version == None)
            ):
            return html.Div(f'''❌ Error: "{filename}" does not seem to be a FERMO
            session file in JSON format, or is somehow malformed.
            '''), None, None
        elif version != FERMO_version:
            df = utils.session_loading_table(params, files, metadata, version)
            return html.Div(f'''❗ Warning: The loaded session file "{filename}"
            has been created using "{df.at[18,'Description']}", while the currently running version is 
            "{FERMO_version}". This might lead to unforseen behaviour of the application. 
            '''), loaded_session_JSON, df.to_dict('records')
        else:
            df = utils.session_loading_table(params, files, metadata, version)
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',}), loaded_session_JSON, df.to_dict('records')

#########################
###CALLBACKS DASHBOARD###
#########################

@callback(
    Output('threshold_values', 'data'),
    Input('rel_intensity_threshold', 'value'),
    Input('convolutedness_threshold', 'value'),
    Input('bioactivity_threshold', 'value'),
    Input('novelty_threshold', 'value'),
)
def read_threshold_values_function(rel_int, conv, bioact, nov,):
    '''Bundle input values'''

    if None not in [rel_int, conv, bioact, nov,]:
        return {
            'rel_int' : float(rel_int),
            'conv' : float(conv),
            'bioact' : float(bioact),
            'nov' : float(nov),
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
        samples_subsets[sample] = utils.generate_subsets(
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
        'Diversity score' : [
            round(
                (
                len(
                    set(sample_stats["cliques_per_sample"][i]).difference(
                        set(sample_stats["set_blank_cliques"])
                        )
                    )
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2) for i in samples],
        'Spec score' : [
            round(
                (
                (len(sample_unique_cliques[i]))
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2) for i in samples],
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
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    return utils.plot_central_chrom(
        selected_sample,
        active_feature_index,
        sample_stats,
        samples,
        samples_subsets)

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

    return utils.plot_clique_chrom(
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
    
    return utils.plot_mini_chrom(
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
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    if isinstance(active_feature_index, int):
        return utils.modify_feature_info_df(
            selected_sample,
            active_feature_id,
            active_feature_index,
            feature_dicts,
            samples,
            )
    else:
        return utils.empty_feature_info_df()

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
        return utils.generate_cyto_elements(
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
        return utils.add_nodedata(nodedata, feature_dicts,)

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
        return utils.add_edgedata(edgedata, feature_dicts,)

@callback(
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
    
        #temporarily convert from JSON to pandas DF
        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')
        
        df = utils.export_sel_peaktable(samples, sel_sample)
        
        return dcc.send_data_frame(df.to_csv, ''.join([sel_sample, '.csv']))

@callback(
    Output("download_all_peak_table", "data"),
    Input("button_all_peak_table", "n_clicks"),
    State('data_processing_FERMO', 'data'),
)
def export_all_samples(n_clicks, contents):
    '''Export peaktables of all samples'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        samples_JSON = contents['samples_JSON']
    
        #temporarily convert from JSON to pandas DF
        samples = dict()
        for sample in samples_JSON:
            samples[sample] = pd.read_json(
                samples_JSON[sample], orient='split')
        
        list_dfs = []
        for sample in samples:
            #call function
            df = utils.export_sel_peaktable(samples, sample)
            df['sample'] = sample
            list_dfs.append(df)
        df_all = pd.concat(list_dfs)
        return dcc.send_data_frame(df_all.to_csv, 'FERMO_all_samples.csv')

@callback(
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
        df = utils.export_features(feature_dicts)
        return dcc.send_data_frame(df.to_csv, 'FERMO_all_features.csv')

@callback(
    Output("export_session_file", "data"),
    Input("button_export_session", "n_clicks"),
    State('data_processing_FERMO', 'data'),
)
def export_all_features(n_clicks, contents):
    '''Export FERMO data as JSON'''
    if n_clicks == 0:
        raise PreventUpdate
    else:
        return dcc.send_string(json.dumps(contents, indent=4), 'FERMO_session.json')

##########
#START APP 
##########


if __name__ == '__main__':
    app.run_server(debug=True)
