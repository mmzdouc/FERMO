import dash
from dash import Dash, html, dcc, Input, Output, State, callback, dash_table, ctx, DiskcacheManager, CeleryManager
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
    color_dict,
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
        ###Stores for routing###
        dcc.Store(id='store_landing'),
        dcc.Store(id='store_processing_slow'),
        dcc.Store(id='store_mzmine'),
        dcc.Store(id='store_loading'),
        ###Stores for data processing###
        dcc.Store(id='data_processing_FERMO'),
        dcc.Store(id='data_storage_FERMO'),
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
    Output('loading_start_cache', 'children'),
    Input('call_dashboard_loading', 'n_clicks'),
    State('upload_session_storage', 'data'),
)
def call_pages_loading(dashboard_loading, session_storage):
    '''Set redirect on page "loading". Can't accept input from other pages'''
    if not dashboard_loading:
        raise PreventUpdate
    elif session_storage is None:
        raise PreventUpdate
    else:
        return html.Div('Started processing, please wait ...')


@callback(
    Output('store_loading', 'data'),
    Output('loaded_data_FERMO', 'data'),
    Input('loading_start_cache', 'children'),
    State('upload_session_storage', 'data'),
)
def function(signal, session_storage):
    if signal is None:
        raise PreventUpdate
    else:
        return '/dashboard', session_storage


        


##########
#PROCESSING 
##########

@callback(
    Output('data_processing_FERMO', 'data'),
    Input('data_storage_FERMO', 'data'),
    Input('loaded_data_FERMO', 'data'),
    )
def routing_processing_loading(storage, loading):
    '''Bundle input values'''
    if ctx.triggered_id == 'data_storage_FERMO':
        return storage
    elif ctx.triggered_id == 'loaded_data_FERMO':
        return loading


@callback(
    Output('store_processing_slow', 'data'),
    Output('data_storage_FERMO', 'data'),
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
        
        storage_JSON_dict = utils.make_JSON_serializable(FERMO_data)
        
        # ~ #save to disk
        # ~ dirname = os.path.dirname(__file__)
        # ~ session_filename = os.path.join(dirname, 'FERMO_session.json',)
        # ~ outfile = open(session_filename, 'w')
        # ~ storage_JSON = json.dump(storage_JSON_dict, outfile, indent=4)
        # ~ outfile.close()
        # ~ print("ALERT: Saved to session file.")
        
        

        return '/dashboard', storage_JSON_dict




##########
#START APP 
##########


if __name__ == '__main__':
    app.run_server(debug=True)
