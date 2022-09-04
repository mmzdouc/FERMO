from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

import styles

params_df = pd.DataFrame({
    'Parameters' : [
        'Mass deviation (in ppm)',
        'Minimal nr of MS<sup>2</sup> peaks',
        'Feature relative intensity filter',
        'Bioactivity factor',
        'Column retention factor',
        ],
    'Values' : 'N/A',
    })




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
                style_data=styles.style_data_table,
                style_data_conditional=styles.style_data_cond_table,
                style_header=styles.style_header_table,
                ),
            style={'display': 'inline-block'},
            ),
        html.Div(id='params_cache', hidden=True)
    ])

def call_mass_dev_dd():
    '''Call estimated mass deviation drop down menu'''
    return html.Div([
        html.Div([
            '''
            Select the estimated mass deviation of your data:
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


def call_peaktable_upload():
    '''Call the peaktable upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button('Upload MZmine3 peaktable (*_full.csv)'),
                    id='upload-peaktable'),
                html.A(
                    html.Div(
                        "?",
                        id="upload-peaktable-tooltip",
                        className="info_dot"
                        ),
                    #DUMMY LINK, SPECIFY CORRECT DOC LINK
                    href='https://github.com/mmzdouc/fermo', 
                    target='_blank',
                    ),
                dbc.Tooltip(
                    html.Div(
                        '''
                        
                        
                        For more information and full reasoning,
                        click this info-button to access the docs.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-peaktable-tooltip",
                    ),
                ]),
            html.Div(id='upload-peaktable-output'),
            html.Hr(),
        ])












def call_start_button():
    '''Call the button that starts FERMO processing'''
    return html.Div([
        dbc.Button(
            "Start FERMO!",
            id='start_button',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])


header_row = html.Div(
    dbc.Row([
        dbc.Col([
                html.Div(
                    html.A([
                        html.Img(
                            src='/assets/Fermo_logo.svg',
                            style={'height':'7.5vh'},
                            ),
                        ],
                        href='https://github.com/mmzdouc/fermo',
                        target="_blank",
                    ),
                ),
            ],
        id="header_col",
        width="True",
        style={'display': 'inline-block'},
        ),
    ],
    id="header_row",
    ),
)

landing_page = html.Div([
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
                #LOAD PREPROCESSED DATA
                html.Div('Placeholder for loading of preprocessed data'),
                #PEAKTABLE UPLOAD FIELD
                call_peaktable_upload(),
                ],
            id="landing_row_2_col_1",
            width=4,
            ),
        #second column#
        dbc.Col([
                #PROCESS RAW DATA W MZMINE3
                html.Div('Placeholder for loading of raw data (Mzmine3)'),
                
            ],
            id="landing_row_2_col_2",
            width=4,
            ),
        #third column#
        dbc.Col([
                #LOAD FROM SESSION FILE
                html.Div('Placeholder for upload from session file'),
            ],
            id="landing_row_2_col_3",
            width=4,
            ),
        ],
    id="landing_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                #SETTINGS/PARAMS GENERAL
                html.Div('Placeholder for settings/parameters'),
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
            ],
            id="landing_row_3_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                #PREVIEW DATA TABLE
                html.Div('Placeholder for preview data table'),
                #PARAMETER TABLE
                call_table_params_cache(),
            ],
            id="landing_row_3_col_2",
            width=6,
            ),
        ],
    id="landing_row_3",
    ),
    ###fourth row###
    dbc.Row([
        dbc.Col([
                #START BUTTON CALCULATION FERMO
                call_start_button(),
            ],
            id="landing_row_4_col_1",
            width=12,
            ),
        ],
    id="landing_row_4",
    ),
])


    
dashboard_page = html.Div([
    html.Div('Dashboard page'),
    ])


footer_row = html.Div(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.A([
                    html.Img(
                        src='/assets/WUR_logo.png',
                        style={'height': '7.5vh'},
                        ),
                    ],
                    href='https://www.wur.nl/en/research-results/chair-groups/plant-sciences/bioinformatics/people.htm',
                    target="_blank",
                    ),
                html.A([
                    html.Img(
                        src='/assets/Marbles_logo.svg',
                        style={'height': '7vh', 'margin': '10px 10px 0px'},
                        ),
                    ],
                    href='https://marblesproject.eu/',
                    target="_blank",
                    ),
                ],
            ),
        ],
        id="footer_col",
        width="True",
        style={'display': 'inline-block'},
        ),
    ],
    id="footer_row",
    ),
)






