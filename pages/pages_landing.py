from dash import html
import dash_bootstrap_components as dbc

def call_processing_page():
    '''Create button that redirects to peaktable processing page'''
    return html.Div([
        dbc.Button(
            "Peaktable processing (standard mode)",
            id='call_processing_button',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])

def call_mzmine_page():
    '''Create button that redirects to MZmine3 preprocessing page'''
    return html.Div([
        dbc.Button(
            "Pre-processing (raw data mode)",
            id='call_mzmine_button',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            disabled=True, #switch on when ready
            ),
        ])

def call_loading_page():
    '''Create the button that redirects to loading page'''
    return html.Div([
        dbc.Button(
            "Session file (loading mode)",
            id='call_loading_button',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            # ~ disabled=True, #switch on when ready
            ),
        ])

def call_landing_header_intro_text():
    '''Div to hold intro text for landing page'''
    return html.H2(
            'LC-MS/MS data analysis and feature prioritization made easy',
        )


def call_landing_intro_text():
    '''Div to hold intro text for landing page'''
    return html.Div([
        html.Div('FERMO is an app for the visualization and analysis of LC-MS/MS metabolomics data.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('''
        FERMO integrates metabolomics data, bioactivity data, and metadata in a combined analysis platform. In each sample, features are assessed for their associatedness with bioactivity, their putative novelty, and the estimated ease of isolation. For these attributes, scores are calculated, and the chemical diversity of the samples is estimated. The resulting metrics allow for pragmatic prioritization of features and samples for further investigation.
        '''),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('''
        FERMO can used in different modes, which can be accessed by clicking the buttons on the bottom of the page.
        '''),
        html.Div(style={'margin-top' : '10px'}),
        html.Div([
            'More information on FERMO can be found in the ',
            html.A('tutorial',
                href='https://github.com/mmzdouc/fermo',
                target="_blank",
                ),
            ' or in the ',
            html.A('documentation.',
                href='https://github.com/mmzdouc/fermo',
                target="_blank",
                ),
            ]),
    ],
    style={
        'line-height' : '1.5',
        'text-align' : 'justify',
        }
    )

def call_landing_intro_workflow():
    '''Div to hold intro workflow for landing page'''

    return html.Div(
            html.Img(
                src='/assets/app-landing-workflow.svg',
                ),
            style={
                'height': '20vh',
                'text-align' : 'center',
                'margin-top' : '30px'
                },
            )

def call_landing_header_peaktable_text():
    '''Div to hold header for peaktable processing start'''
    return html.H3(
            'Peaktable processing (standard mode)',
            style={'text-align' : 'center',}
        )

def call_landing_peaktable_text():
    '''Div to hold intro text on peaktable processing'''
    return html.Div([
        html.Div(style={'margin-top' : '10px'}),
        html.Div('Processes user-provided data via the standard workflow.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('This mode is intended for users with some experience in metabolomics data processing.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('''
        It requires a MZmine3 formatted peaktable and a corresponding file in the .mgf-format containing MS/MS data. Optionally, users can also provide a table containing metadata, and a table containing bioactivity data.
        '''),
        html.Div(style={'margin-top' : '10px'}),
    ],
    style={
        'line-height' : '1.5',
        'text-align' : 'center',
        },
    )

def call_landing_header_mzmine_text():
    '''Div to hold header mzmine processing start'''
    return html.H3(
            'Data pre-processing (raw data mode)',
            style={'text-align' : 'center',}
        )

def call_landing_mzmine_text():
    '''Div to hold text mzmine processing start'''
    return html.Div([
        html.Div(style={'margin-top' : '10px'}),
        html.Div('Pre-processes "raw" LC-MS/MS data with MZmine3 before FERMO.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('This mode is intended for users with limited experience in metabolomics data processing.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('''
        This mode requires the user to copy 'raw' LC-MS/MS data in the .mzXML or .mzML format in the INPUT folder of FERMO. The data will be first pre-processed using MZmine3, resulting in a peaktable and .mgf-file, which are then analyzed by FERMO. This mode accepts metadata and bioactivity data too.
        '''),
        html.Div(style={'margin-top' : '10px'}),
    ],
    style={
        'line-height' : '1.5',
        'text-align' : 'center',
        },
    )

def call_landing_header_loading_text():
    '''Div to hold header loading start'''
    return html.H3(
            'Restart session (loading mode)',
            style={'text-align' : 'center',}
        )

def call_landing_loading_text():
    '''Div to hold text loading start'''
    return html.Div([
        html.Div(style={'margin-top' : '10px'}),
        html.Div('Reloads a session file previously created by FERMO'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('This mode is intended for users who want to reload a previous FERMO session.'),
        html.Div(style={'margin-top' : '10px'}),
        html.Div('''
        This mode requires to load a session file. Attention: only load session files from trusted sources, such as your own session files, or session files from close collaborators. Do not attempt to load session files from insecure sources (i.e., the internet).
        '''),
        html.Div(style={'margin-top' : '10px'}),
    ],
    style={
        'line-height' : '1.5',
        'text-align' : 'center',
        },
    )

def call_landing_peaktable_icon():
    '''Div to hold icon peaktable start'''
    return html.Div(
            html.Img(
                src='/assets/icon-peaktable-processing.svg',
                style={'height': '10vh'},
                ),
            style={
                'text-align' : 'center',
                'margin-top' : '20px',
                },
            )
            
def call_landing_mzmine_icon():
    '''Div to hold icon mzmine start'''
    return html.Div(
            html.Img(
                src='/assets/icon-mzmine-processing.svg',
                style={'height': '10vh'},
                ),
            style={
                'text-align' : 'center',
                'margin-top' : '20px',
                },
            )
            
def call_landing_loading_icon():
    '''Div to hold icon loading start'''
    return html.Div(
            html.Img(
                src='/assets/icon-loading-processing.svg',
                style={'height': '10vh'},
                ),
            style={
                'text-align' : 'center',
                'margin-top' : '20px',
                },
            )





landing = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
            html.Div([
                call_landing_header_intro_text(),
                call_landing_intro_text(),
            ],
            style={
                'margin-left':'30px',
                'margin-top':'30px',
                },
            )
                
                ],
            id="landing_row_1_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                call_landing_intro_workflow(),
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
            html.Div([
                call_landing_header_peaktable_text(),
                call_landing_peaktable_icon(),
                call_landing_peaktable_text(),
                ],
                style={
                    'margin-left':'40px',
                    'margin-right':'40px',
                    }
                ),
            ],
            id="landing_row_2_col_1",
            width=4,
            ),
        #second column#
        dbc.Col([
            html.Div([
                call_landing_header_mzmine_text(),
                call_landing_mzmine_icon(),
                call_landing_mzmine_text(),
                ],
                style={
                    'margin-left':'40px',
                    'margin-right':'40px',
                    }
                ),
            ],
            id="landing_row_2_col_2",
            width=4,
            ),
        #third column#
        dbc.Col([
            html.Div([
                call_landing_header_loading_text(),
                call_landing_loading_icon(),
                call_landing_loading_text(),
                ],
                style={
                    'margin-left':'40px',
                    'margin-right':'40px',
                    }
                ),
            ],
            id="landing_row_2_col_3",
            width=4,
            ),
        ],
    id="landing_row_2",
    ),
    ###third row###
    dbc.Row([
        dbc.Col([
            call_processing_page(),
            ],
            id="landing_row_3_col_1",
            width=4,
            ),
        #second column#
        dbc.Col([
            call_mzmine_page(),
            ],
            id="landing_row_3_col_2",
            width=4,
            ),
        #third column#
        dbc.Col([
            call_loading_page(),
            ],
            id="landing_row_3_col_3",
            width=4,
            ),
        ],
    id="landing_row_3",
    ),
])


    










