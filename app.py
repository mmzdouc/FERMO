import dash
from dash import Dash, html, dcc, Input, Output, callback, dash_table, ctx, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle
import time
import os
import json
import pandas as pd

#Required for background callbacks
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)




#local modules
import callbacks

import utils

from variables import (
    params_dict,
    input_file_store,
    style_data_table,
    style_data_cond_table,
    style_header_table,
)


from pages.pages_header_footer import footer_row, header_row
from pages.pages_landing import landing
from pages.pages_dashboard import dashboard
from pages.pages_processing import processing
from pages.pages_mzmine import mzmine
from pages.pages_loading import loading


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

framework_app = dbc.Container([
    header_row,
    #content row
    html.Div([
        dcc.Store(id='store_landing'),
        dcc.Store(id='store_processing_slow'),
        dcc.Store(id='store_mzmine'),
        dcc.Store(id='store_loading'),
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


##########
#ROUTING
##########


@callback(
    Output('url', 'pathname'),
    Input('store_landing', 'data'),
    Input('store_processing_slow', 'data'),
    Input('store_mzmine', 'data'),
    Input('store_loading', 'data'),
)
def return_pagename(landing, processing_slow, mzmine, loading):
    '''Helper function to combine callbacks from different pages'''

    if ctx.triggered_id == 'store_landing':
        return landing
    elif ctx.triggered_id == 'store_processing_slow':
        return processing_slow
    elif ctx.triggered_id == 'store_mzmine':
        return mzmine
    elif ctx.triggered_id == 'store_loading':
        return loading
    
    
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    '''Routing function'''
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
    Output('store_landing', 'data'),
    Input('call_processing_button', 'n_clicks'),
    Input('call_mzmine_button', 'n_clicks'),
    Input('call_loading_button', 'n_clicks'),
)
def call_pages_landing(processing, mzmine, loading, ):
    '''Set redirect on page landing. Can't accept input from other pages'''
    if not any((processing,  mzmine, loading, )):
        raise PreventUpdate
    else:
        if processing:
            return '/processing'
        elif mzmine:
            return '/mzmine'
        elif loading:
            return '/loading'

@callback(
    Output('processing_start_cache', 'children'),
    Input('call_dashboard_processing', 'n_clicks'),
)
def function(dashboard_processing):
    '''Set redirect on page "processing". Can't accept input from other pages'''
    if not dashboard_processing:
        raise PreventUpdate
    elif (
    (input_file_store['peaktable'] is None) 
    or
    (input_file_store['mgf'] is None)
    ):
        raise PreventUpdate
    else:
        return html.Div('Started processing, please wait ...')

@callback(
    Output('store_mzmine', 'data'),
    Input('call_dashboard_mzmine', 'n_clicks'),
)
def call_pages_mzmine(dashboard_mzmine):
    '''Set redirect on page "mzmine". Can't accept input from other pages'''
    if not dashboard_mzmine:
        raise PreventUpdate
    else:
        return '/dashboard'

@callback(
    Output('store_loading', 'data'),
    Input('call_dashboard_loading', 'n_clicks'),
)
def call_pages_loading(dashboard_loading):
    '''Set redirect on page "loading". Can't accept input from other pages'''
    if not dashboard_loading:
        raise PreventUpdate
    else:
        return '/dashboard'

##########
#PROCESSING 
##########

@callback(
    Output('store_processing_slow', 'data'),
    Input('processing_start_cache', 'children'),
    background=True,
    manager=background_callback_manager,
    running=[(Output("call_dashboard_processing", "disabled"), True, False),],
)
def function(signal):
    '''Main function for peaktable processing'''
    if signal is None:
        raise PreventUpdate
    else:
        FERMO_data = utils.peaktable_processing(
            input_file_store,
            params_dict,
            )
        
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
            } 
        
        #save to disk
        dirname = os.path.dirname(__file__)
        session_filename = os.path.join(dirname, 'FERMO_session.json',)
        outfile = open(session_filename, 'w')
        storage_JSON = json.dump(storage_JSON_dict, outfile, indent=4)
        outfile.close()
        print("ALERT: Saved to session file.")
        
        #####
        
        #Load session file from disk
        with open('FERMO_session.json') as json_file:
            loaded_JSON_dict = json.load(json_file)
        
        #convert samples from JSON to df
        samples_DF = dict()
        for sample in loaded_JSON_dict['samples_JSON']:
            samples_DF[sample] = pd.read_json(loaded_JSON_dict['samples_JSON'][sample], orient='split')
        
        print(samples_DF)
        
        
        '''RESTART HERE
        -move loading module to its respective page
        -put filenames and params used in separate dict, save also to JSON
        
        '''
        
        
        # ~ samples_JSON = dict()
        # ~ for sample in FERMO_data['samples']:
            # ~ samples_JSON[sample] = FERMO_data['samples'][sample].to_json(
                # ~ orient='split')
        
        
        
        
        # ~ for i in loaded_JSON_dict['feature_dicts']:
            # ~ print(i)
        
        
        
        
        #load storage data structure
        
        
        #continue
        
        
        
        # ~ samples_from_JSON = dict()
        # ~ for sample in samples_JSON:
            # ~ samples_from_JSON[sample] = pd.read_json(
                # ~ samples_JSON[sample],
                # ~ )
        
        # ~ FERMO_data = {
        # ~ 'feature_dicts' : feature_dicts,
        # ~ 'samples' : samples,
        # ~ 'sample_stats' : sample_stats,
        # ~ }
        
        
        
        
        
        # ~ session_filename = os.path.join(dirname, 'FERMO_cache.session',)
        
        
        
        #TO DO:
        #convert samples to json
        #dump storage file as JSON
        #convert back from JSON
        #return value to app.py
        
        # ~ session_filename = os.path.join(dirname, 'FERMO_cache.session',)
        # ~ outfile = open(session_filename, 'wb')
        # ~ pickle.dump(storage_input, outfile)
        # ~ outfile.close()
        # ~ print("ALERT: Saved to session (cache) file.")
        
        
        
        #store FERMO data in browser in separate Store container
        #(two output functions)

        #return two outputs - routing and separate storage for FERMO_data
        return '/dashboard'




##########
#START APP 
##########


if __name__ == '__main__':
    app.run_server(debug=True)
