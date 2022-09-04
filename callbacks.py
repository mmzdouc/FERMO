from dash import Input, Output, callback, dcc, dash_table, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle

import sys
import os


import io
import base64

from layouts import params_df

@callback(
    Output(component_id='url', component_property='pathname'),
    Input(component_id='start_button', component_property='n_clicks'),
)
def start_calculation(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        print(params_df)
        
        
        
        
        #READ PRE-SPECIFIED INPUT FOLDER
        dirname = os.path.dirname(__file__)
        input_folder = os.path.join(dirname, 'INPUT',)
        
        assert os.path.exists(input_folder), 'ERROR'
        
        list_input_files = os.listdir(input_folder)
        
        print(list_input_files)
        
        
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
    )
def bundle_into_cache(
    mass_dev, 
    min_ms2, 
    feat_int_filt,
    bioact_fact,
    column_ret_fact,
    ):
    '''Bundle input values'''
    return {
    'mass_dev' : mass_dev,
    'min_ms2' : min_ms2,
    'feat_int_filt' : feat_int_filt,
    'bioact_fact' : bioact_fact,
    'column_ret_fact' : column_ret_fact,
    
    }


@callback(
    Output('table_params', 'data'),
    Input('params_cache', 'component')
)
def update_output(params_cache):
    
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
        return params_df.to_dict('records')
    


# ~ id='upload-peaktable',
# ~ id='upload-peaktable-output',
    
@callback(
    Output('upload-peaktable-output', 'children'),
    Input('upload-peaktable', 'contents'),
    State('upload-peaktable', 'filename'),
    State('upload-peaktable', 'last_modified')
)
def update_output(contents, filename, last_modified):
    
    if contents is not None:
        
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)
        
        decoded = io.StringIO(decoded.decode('utf-8'))
        
        print(decoded)
        
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
