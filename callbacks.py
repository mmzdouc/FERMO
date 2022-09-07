from dash import Input, Output, callback, dcc, dash_table, State, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle

import sys
import os
import pandas as pd
import io
import base64


#local functions
from variables import params_df, uploads_df, input_file_store
import utils


@callback(
    Output(component_id='url', component_property='pathname'),
    Input(component_id='start_button_table', component_property='n_clicks'),
)
def start_calculation(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        
        #get the parameters -> params_df
        #get the input files -> input_file_store
        #load in the main -> build step by step
        
        #load in all four files
        
        
        
        #write a catch that prevents running FERMO without any input
        
        
        
        
        
        
        
        
        #put the decision tree here
        #for first option, the peaktable and optionally, the mgf
        #and the metadata and bioativity file - probably best to do 
        #some
        #
              
        
        # ~ #READ PRE-SPECIFIED INPUT FOLDER
        # ~ dirname = os.path.dirname(__file__)
        # ~ input_folder = os.path.join(dirname, 'INPUT',)
        
        # ~ assert os.path.exists(input_folder), 'ERROR'
        
        # ~ list_input_files = os.listdir(input_folder)
        
        # ~ print(list_input_files)
        
        
        #STORAGE DATA BY PICKLE DUMP
        # ~ storage_input = 'Hakuna matata'
        # ~ outfile = open('temp', 'wb')
        # ~ pickle.dump(storage_input, outfile)
        # ~ outfile.close()
        # ~ print("ALERT: Saved to session (cache) file.")

        #READ 
        
        
        
        
        return '/dashboard'

@callback(
    Output('params_cache', 'component'),
    Input('mass_dev_dd', 'value'),
    Input('min_ms2_inpt', 'value'),
    Input('feat_int_filt_inp', 'value'),
    Input('bioact_fact_inp', 'value'),
    Input('column_ret_fact_inp', 'value'),
    Input('spec_sim_tol_inp', 'value'),
    Input('spec_sim_score_cutoff_inp', 'value'),
    Input('spec_sim_max_links_inp', 'value'),
    Input('spec_sim_min_match_inp', 'value'),
    )
def bundle_into_cache(
    mass_dev, 
    min_ms2, 
    feat_int_filt,
    bioact_fact,
    column_ret_fact,
    spec_sim_tol_inp,
    spec_sim_score_cutoff_inp,
    spec_sim_max_links_inp,
    spec_sim_min_match_inp,
    ):
    '''Bundle input values'''
    return {
    'mass_dev' : mass_dev,
    'min_ms2' : min_ms2,
    'feat_int_filt' : feat_int_filt,
    'bioact_fact' : bioact_fact,
    'column_ret_fact' : column_ret_fact,
    'spec_sim_tol' : spec_sim_tol_inp,
    'spec_sim_score_cutoff' : spec_sim_score_cutoff_inp,
    'spec_sim_max_links' : spec_sim_max_links_inp,
    'spec_sim_min_match' : spec_sim_min_match_inp,
    
    }


@callback(
    Output('table_params', 'data'),
    Input('params_cache', 'component')
)
def update_output(params_cache):
    
    #maybe change to a more compact expression using a for loop?

    if params_cache is not None:
        params_df.at[0, "Values"] = (params_cache['mass_dev']
            if params_cache['mass_dev'] is not None
            else 20)
        params_df.at[1, "Values"] = (params_cache['min_ms2']
            if params_cache['min_ms2'] is not None
            else 0)
        params_df.at[2, "Values"] = (params_cache['feat_int_filt']
            if params_cache['feat_int_filt'] is not None
            else 0)
        params_df.at[3, "Values"] = (params_cache['bioact_fact']
            if params_cache['bioact_fact'] is not None
            else 0)
        params_df.at[4, "Values"] = (params_cache['column_ret_fact']
            if params_cache['column_ret_fact'] is not None
            else 0)
        params_df.at[5, "Values"] = (params_cache['spec_sim_tol']
            if params_cache['spec_sim_tol'] is not None
            else 0)
        params_df.at[6, "Values"] = (params_cache['spec_sim_score_cutoff']
            if params_cache['spec_sim_score_cutoff'] is not None
            else 0)
        params_df.at[7, "Values"] = (params_cache['spec_sim_max_links']
            if params_cache['spec_sim_max_links'] is not None
            else 0)
        params_df.at[8, "Values"] = (params_cache['spec_sim_min_match']
            if params_cache['spec_sim_min_match'] is not None
            else 0)
        return params_df.to_dict('records')


@callback(
    Output('table_uploaded_files', 'data'),
    Input('upload-peaktable-output', 'children')
)
def update_output(params_cache):
    return uploads_df.to_dict('records')

    
@callback(
    Output('upload-peaktable-output', 'children'),
    Input('upload-peaktable', 'contents'),
    State('upload-peaktable', 'filename'),
)
def update_output(contents, filename):
    '''Read a user-provided peaktable, assign to dict, return Div'''
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            #read peaktable
            peaktable = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            #test for expected fields
            utils.assert_peaktable_format(peaktable)
            #assign to storage, reporting
            input_file_store['peaktable'] = peaktable
            input_file_store['peaktable_name'] = filename
            uploads_df.at[0, "Status"] = 'Ready'
            return html.Div(f'"{filename}" successfully loaded.')
        except:
            input_file_store['peaktable'] = None
            input_file_store['peaktable_name'] = None
            uploads_df.at[0, "Status"] = 'Not ready'
            return html.Div(f'"{filename}" wrongly formatted.')




@callback(
    Output('upload-mgf-output', 'children'),
    Input('upload-mgf', 'contents'),
    State('upload-mgf', 'filename'),
    State('upload-mgf', 'last_modified')
)
def update_output(contents, filename, last_modified):
    
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)
        
        
        decoded = io.StringIO(decoded.decode('utf-8'))
        
        
        return [
        decoded,
        filename,
        last_modified
        ]
        
        
@callback(
    Output('upload-bioactiv-output', 'children'),
    Input('upload-bioactiv', 'contents'),
    State('upload-bioactiv', 'filename'),
    State('upload-bioactiv', 'last_modified')
)
def update_output(contents, filename, last_modified):
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)
        
        decoded = io.StringIO(decoded.decode('utf-8'))

        
        return [
        decoded,
        filename,
        last_modified
        ]
        
        
@callback(
    Output('upload-metadata-output', 'children'),
    Input('upload-metadata', 'contents'),
    State('upload-metadata', 'filename'),
    State('upload-metadata', 'last_modified')
)
def update_output(contents, filename, last_modified):
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)
        
        decoded = io.StringIO(decoded.decode('utf-8'))
                
        return [
        decoded,
        filename,
        last_modified
        ]


@callback(
    Output('upload-session-output', 'children'),
    Input('upload-session', 'contents'),
    State('upload-session', 'filename'),
    State('upload-session', 'last_modified')
)
def update_output(contents, filename, last_modified):
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)
        
        decoded = io.StringIO(decoded.decode('utf-8'))
        
        return [
        decoded,
        filename,
        last_modified
        ]

# ~ @callback(
    # ~ Output('params_loading', 'children'),
    # ~ Input('url', 'pathname'),
# ~ )
# ~ def display_params(pathname):
    # ~ if pathname == '/dashboard':
        # ~ try:
            # ~ infile = open('temp', 'rb')
            # ~ session_FERMO = pickle.load(infile) 
            # ~ infile.close()
            # ~ return session_FERMO
        # ~ except:
            # ~ return 'NO file temp found'
