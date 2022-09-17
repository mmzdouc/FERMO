import dash
from dash import Input, Output, callback, dcc, dash_table, State, html, ctx, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle

from pyteomics import mgf

import sys
import os
import pandas as pd
import io
import base64


####LOCAL MODULES AND VARS

import utils

from variables import (
    params_df,
    input_file_store,
    style_data_table,
    style_data_cond_table,
    style_header_table,
)


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
def bundle_into_cache(
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
    Output('out_params_assignment', 'children'),
    Input('params_cache', 'component')
)
def update_output(params_cache):
    '''Assign set params to table, with sanity check for None'''

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
            
        return html.Div()

@callback(
    Output('upload-peaktable-output', 'children'),
    Input('processing-upload-peaktable', 'contents'),
    State('processing-upload-peaktable', 'filename'),
)
def function(contents, filename):
    '''Peaktable parsing and format check'''
    
    if contents is None:
        return html.Div('No peaktable loaded.',)
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            peaktable = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['peaktable'] = None
            input_file_store['peaktable_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        return_assert = utils.assert_peaktable_format(peaktable, filename)
        
        peaktable.rename(
            columns={
                'id' : 'feature_ID',
                'mz' : "precursor_mz",
                'rt' : "retention_time",
                },
            inplace=True,
            )
            
        if return_assert is not None:
            input_file_store['peaktable'] = None
            input_file_store['peaktable_name'] = None
            return return_assert
        else:
            input_file_store['peaktable'] = peaktable
            input_file_store['peaktable_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })

@callback(
    Output('upload-mgf-output', 'children'),
    Input('processing-upload-mgf', 'contents'),
    State('processing-upload-mgf', 'filename'),
)
def function(contents, filename):
    '''mgf file parsing and format check'''
    
    if contents is None:
        return html.Div('No .mgf-file loaded.')
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
            
            input_file_store['mgf'] = ms2spectra
            input_file_store['mgf_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })
            
        except:
            input_file_store['mgf'] = None
            input_file_store['mgf_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" is not a mgf or is erroneously formatted.
                 Please check the file and try again.
                ''')

@callback(
    Output('upload-bioactiv-output', 'children'),
    Input('upload-bioactiv', 'contents'),
    State('upload-bioactiv', 'filename'),
    Input('bioact_type', 'value'),
)
def function(contents, filename, value):
    '''Bioactivity table parsing and format check'''
    if contents is None:
        return html.Div('No bioactivity table loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            bioactiv_table = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['bioactivity'] = None
            input_file_store['bioactivity_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        
        if value is None:
            return html.Div(
                f'''
                ❌ Error: Please specify the bioactivity table format.
                Currently, the value is {value}.
                ''')
        
        return_assert = utils.assert_bioactivity_format(
            bioactiv_table, 
            filename,
            )
        
        if return_assert is not None:
            input_file_store['bioactivity'] = None
            input_file_store['bioactivity_name'] = None
            return return_assert
        else:
            converted_df = utils.parse_bioactiv_conc(bioactiv_table, value)
            input_file_store['bioactivity'] = converted_df
            input_file_store['bioactivity_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })



@callback(
    Output('store_bioact_type', 'children'),
    Input('bioact_type', 'value'),
)
def function(value):
    '''Stores the value of bioactivity data format'''
    return html.Div(value)


@callback(
    Output('upload-metadata-output', 'children'),
    Input('upload-metadata', 'contents'),
    State('upload-metadata', 'filename'),
)
def function(contents, filename,):
    '''Metadata table parsing and format check'''
    if contents is None:
        return html.Div('No metadata table loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    
        try:
            metadata_table = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['metadata'] = None
            input_file_store['metadata_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        
        return_assert = utils.assert_metadata_format(
            metadata_table, 
            filename,
            )
        
        if return_assert is not None:
            input_file_store['metadata'] = None
            input_file_store['metadata_name'] = None
            return return_assert
        else:
            input_file_store['metadata'] = metadata_table
            input_file_store['metadata_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })


@callback(
    Output('upload-session-output', 'children'),
    Input('upload-session', 'contents'),
    State('upload-session', 'filename'),)
def function(contents, filename):
    return html.Div(
                f'''
                SESSION FILE UPLOAD NOT YET ACTIVE
                ''')









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
        
        
        
        
