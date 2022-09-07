from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

from variables import params_df, uploads_df, input_file_store
from variables import style_data_table, style_data_cond_table, style_header_table



#FUNCTIONS

def call_table_params_cache():
    '''Call set parameter visualization table '''
    return html.Div([
        html.Div(
            dash_table.DataTable(
                id='table_params',
                columns=[{
                    "name": i, 
                    "id": i, 
                    "presentation" : 'markdown'}
                for i in params_df.columns],
                markdown_options={"html": True},
                style_as_list_view=True,
                style_data=style_data_table,
                style_data_conditional=style_data_cond_table,
                style_header=style_header_table,
                ),
            style={
                'display': 'inline-block',
                'float': 'left',
                },
            ),
        html.Div(id='params_cache', hidden=True)
    ])
    
def call_uploaded_files_cache():
    '''Call uploaded files visualization table '''
    return html.Div([
        html.Div(
            dash_table.DataTable(
                id='table_uploaded_files',
                columns=[{
                    "name": i, 
                    "id": i, 
                    "presentation" : 'markdown'}
                for i in uploads_df.columns],
                markdown_options={"html": True},
                style_as_list_view=True,
                style_data=style_data_table,
                style_data_conditional=style_data_cond_table,
                style_header=style_header_table,
                ),
            style={
                'display': 'inline-block', 
                'float': 'right'},
            ),
    ])

def call_mass_dev_dd():
    '''Call estimated mass deviation drop down menu'''
    return html.Div([
        html.Div([
            '''
            Select the estimated mass deviation of your data (in ppm):
            ''',
            html.A(
                html.Div(
                    "?",
                    id="mass_dev_dd_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''
                    Used as precision threshold during different 
                    calculation steps, such as ion adduct 
                    calculation. For more information, 
                    click this info-button to access the docs.
                    ''',
                    ),
                placement='right',
                className='info_dot_tooltip',
                target="mass_dev_dd_tooltip",
            ),
        dcc.Dropdown(
            id='mass_dev_dd',
            options=[
                {'label': '30 ppm', 'value': 30},
                {'label': '20 ppm', 'value': 20},
                {'label': '15 ppm', 'value': 15},
                {'label': '10 ppm', 'value': 10},
                {'label': '5 ppm', 'value': 5},
                {'label': '2 ppm', 'value': 2},
                ],
            value=20,
            ),
        ])


def call_min_ms2_inpt():
    '''Call minimal nr ms2 fragments input field'''
    return html.Div([
        html.Div([ 
            '''
            Minimal required number of fragments 
            per MS² spectrum:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="min_ms2_inpt_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Quality control parameter.
                If a MS/MS spectrum does not meet the
                requirement, it is dropped, and the
                associated feature is considered MS1 only. 
                MS/MS spectra with a low number of peaks 1)
                have low information content and 2) 
                may lead to false positive similarity 
                assumptions. For more information, 
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="min_ms2_inpt_tooltip",
            ),
        dbc.Input(
            id='min_ms2_inpt',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=8, 
            min=0,
            step=1,
            ),
        ])

def call_feat_int_filt():
    '''Call feature intensity filter input field'''
    return html.Div([
        html.Div([ 
            '''
            Enter the feature relative intensity filter:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="feat_int_filt_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Value used to filter out low-intensity features 
                ('cut the grass'). Indicates the minimal 
                relative intensity (relative to the feature
                with the highest intensity in the sample)
                a feature must have to be considered for
                further analysis. A value of
                0.05 would exclude all features with a 
                relative intensity below 0.05, i.e. the
                bottom 5% of features; 
                a value of 0 would include all
                features. By default, this value is 0,
                and should be chosen with respect to the 
                underlying data. 
                For more information, 
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="feat_int_filt_tooltip",
            ),
        dbc.Input(
            id='feat_int_filt_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0, 
            min=0,
            max=0.99,
            step=0.01,
            ),
        ])

def call_bioact_fact_inp():
    '''Call the bioactivity factor input field'''
    return html.Div([
        html.Div([ 
            '''
            Enter the bioactivity factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="bioact_fact_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Factor used in the identification of 
                bioactivity-associated features (if
                bioactivity data was provided). 
                If a feature
                was detected in both bioactive and inactive
                samples, how many times must the feature
                be more intense in the active sample with the lowest
                activity
                than the highest intensity detected in in the 
                inactive samples to be still 
                considered bioactivity-associated. 
                This allows to consider sub-active 
                concentrations.
                For example, a value of 10 would 
                mean that the intensity of a feature must 
                be 10 times higher in a bioactive sample than
                in an inactive sample to be considered 
                bioactivity-associated.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="bioact_fact_tooltip",
            ),
        dbc.Input(
            id='bioact_fact_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            step=1,
            ),
        ])


def call_column_ret_fact_inp():
    '''Call the column retention factor input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the column retention factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="column_ret_fact_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Factor used in the identification of 
                medium-blank/sample-blank associated features (if
                metadata was provided). 
                If a feature
                was detected in both authentic samples and 
                medium/sample blanks, how many times must the feature
                be more intense in sample than in a blank to be 
                still considered sample-associated.
                This calculation takes into account retention of
                compounds by the chromatography column and bleed into
                blank analysis runs. 
                For example, a column retention factor of 10 would mean
                that the average intensity of the features across 
                samples must be 10 times higher than the average 
                intensity across blanks.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="column_ret_fact_tooltip",
            ),
        dbc.Input(
            id='column_ret_fact_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            step=1,
            ),
        ])

def call_spec_sim_tol_inp():
    '''Call the spectrum similarity tolerance input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the spectrum similarity tolerance:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_tol_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Tolerance in m/z used in the calculation of spectra 
                similarity scores between MS2 spectra. Two peaks will be 
                considered a match if their difference is less then 
                or equal to the m/z tolerance. Dependent on the 
                precision and mass deviation of the instrument.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_tol_tooltip",
            ),
        dbc.Input(
            id='spec_sim_tol_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0.1, 
            min=0,
            step=0.01,
            ),
        ])

def call_spec_sim_score_cutoff_inp():
    '''Call the spectrum similarity score cutoff input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the spectrum similarity score cutoff:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_score_cutoff_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Score cutoff used in the evaluation of modified 
                cosine scores between MS2 spectra. Two spectra will be 
                considered related only if their score exceeds the 
                cutoff threshold. Therefore, this parameter controls 
                how strict the similarity between two spectra must be.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_score_cutoff_tooltip",
            ),
        dbc.Input(
            id='spec_sim_score_cutoff_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0.8, 
            min=0,
            max=1,
            step=0.01,
            ),
        ])

def call_spec_sim_max_links_inp():
    '''Call the spectrum similarity maximal links input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the maximal number of spectrum similarity links:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_max_links_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Maximal number of links to other nodes, per node. 
                Makes spectral similarity network less convoluted since
                it restricts the number of links between nodes to the 
                highest n ones.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_max_links_tooltip",
            ),
        dbc.Input(
            id='spec_sim_max_links_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            step=1,
            ),
        ])

def call_spec_sim_min_match_inp():
    '''Call the spectrum similarity minimal matched peaks input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the minimum number of matched peaks used 
            in spectrum similarity calculation:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_min_match_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                In spectrum similarity matching, the minimum number of 
                peaks that have to be matched between two spectra to be
                considered a match.
                For more information and full reasoning,
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_min_match_tooltip",
            ),
        dbc.Input(
            id='spec_sim_min_match_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=8, 
            min=0,
            step=1,
            ),
        ])


def call_peaktable_upload():
    '''Call the peaktable upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload peaktable (*_quant_full.csv)',
                        id="upload-peaktable-tooltip",
                        ),
                    id='upload-peaktable'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        MZmine3 style peaktable with the 
                        '_quant_full.csv' suffix
                        (exported in the FULL/ALL mode).
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-peaktable-tooltip",
                    ),
                ]),
        ])

def call_mgf_upload():
    '''Call the mgf upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload .mgf file (*.mgf)',
                        id="upload-mgf-tooltip",
                        ),
                    id='upload-mgf'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        MZmine3 style .mgf-file containing
                        tandem mass (MS/MS) spectra, accompanying
                        the peaktable. Generated through MZmine3 export.
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-mgf-tooltip",
                    ),
                ]),
            html.Div(id='upload-mgf-output'),
            html.Hr(),
        ])

def call_bioactiv_upload():
    '''Call the bioactivity upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload bioactivity table (*.csv)',
                        id="upload-bioactiv-tooltip",
                        ),
                    id='upload-bioactiv'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Bioactivity annotation file in .csv format.
                        FERMO expects on each row a sample name and
                        bioactivity information, which can be in three
                        different formats: 1) the signal word 'active'; 
                        OR 2) a positive integer (whole) number, with
                        the sample with the highest integer considered
                        most active; OR a positive float (dot) number,
                        with the sample with the lowest float considered
                        most active. 
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-bioactiv-tooltip",
                    ),
                ]),
            html.Div(id='upload-bioactiv-output'),
            html.Hr(),
        ])

def call_metadata_upload():
    '''Call the metadata upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload metadata table (*.csv)',
                        id="upload-metadata-tooltip",
                        ),
                    id='upload-metadata'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Metadata annotation file in .csv format.
                        Marks the files that should be considered blanks.
                        FERMO expects on each row a sample name 
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-metadata-tooltip",
                    ),
                ]),
            html.Div(id='upload-metadata-output'),
            html.Hr(),
        ])


def call_session_upload():
    '''Call the session upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload FERMO session file (*.session)',
                        id="upload-session-tooltip",
                        ),
                    id='upload-session'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Load a previously created FERMO session file.
                        ONLY LOAD SESSION FILES FROM TRUSTED SOURCES!
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-session-tooltip",
                    ),
                ]),
            html.Div(id='upload-session-output'),
            html.Hr(),
        ])





def call_start_button_table():
    '''Call the button that starts FERMO processing'''
    return html.Div([
        dbc.Button(
            "Start FERMO directly!",
            id='start_button_table',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])

def call_start_button_mzmine():
    '''Call the button that starts MZmine3 processing, followed by FERMO'''
    return html.Div([
        dbc.Button(
            "Start MZmine3 -> FERMO!",
            id='start_button_mzmine',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])

def call_start_button_loading():
    '''Call the button that loads FERMO session file'''
    return html.Div([
        dbc.Button(
            "Load FERMO session file!",
            id='start_button_loading',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])




landing = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for introduction text on FERMO'),
                ],
            id="landing_row_1_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                #FLOWCHART OF FERMO ANALYSIS
                html.Div('Placeholder for flowchart of FERMO analysis'),
                ],
            id="landing_row_1_col_2",
            width=6,
            ),
        ],
    id="landing_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                #SETTINGS/PARAMS GENERAL
                html.Div('Placeholder for settings/parameters:'),
                #MASS DEVIATION
                call_mass_dev_dd(),
                #MIN MS2 FRAGMENTS
                call_min_ms2_inpt(),
                #FEATURE RELATIVE INTENSITY FILTER
                call_feat_int_filt(),
                #BIOACTIVITY FACTOR
                call_bioact_fact_inp(),
                #COLUMN RETENTION FACTOR
                call_column_ret_fact_inp(),
                #SPECTUM SIMILARITY TOLERANCE
                call_spec_sim_tol_inp(),
                #SPECTUM SIMILARITY SCORE CUTOFF
                call_spec_sim_score_cutoff_inp(),
                #SPECTUM SIMILARITY MAXIMUM NUMBER OF LINKS
                call_spec_sim_max_links_inp(),
                #SPECTUM SIMILARITY MINIMUM NUMBER OF MATCHED PEAKS
                call_spec_sim_min_match_inp(),
            ],
            id="landing_row_2_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                #PREVIEW DATA TABLE
                html.Div('Placeholder for preview data table'),
                #PARAMETER TABLE
                call_table_params_cache(),
                #UPLOADED FILES TABLE
                call_uploaded_files_cache(),
            ],
            id="landing_row_2_col_2",
            width=6,
            ),
        ],
    id="landing_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                #PEAKTABLE UPLOAD FIELD
                call_peaktable_upload(),
                html.Div(id='upload-peaktable-output'),
                html.Hr(),
                #MGF UPLOAD FIELD
                call_mgf_upload(),
                #BIOACTIVITY UPLOAD FIELD
                call_bioactiv_upload(),
                #METADATA UPLOAD FIELD
                call_metadata_upload(),
                #START BUTTON CALCULATION FERMO - PEAKTABLE
                call_start_button_table(),
                ],
            id="landing_row_3_col_1",
            width=4,
            ),
        #second column#
        dbc.Col([
                #PROCESS RAW DATA W MZMINE3
                html.Div('Placeholder for preprocessing of raw data (Mzmine3)'),
                #START BUTTON MZMINE3 + FERMO
                call_start_button_mzmine(),
            ],
            id="landing_row_3_col_2",
            width=4,
            ),
        #third column#
        dbc.Col([
                html.Div('Placeholder for loading from session file'),
                #LOAD FROM SESSION FILE
                call_session_upload(),
                #START BUTTON LOADING
                call_start_button_loading(),
            ],
            id="landing_row_3_col_3",
            width=4,
            ),
        ],
    id="landing_row_3",
    ),
])


    










