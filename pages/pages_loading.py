from dash import html, dcc
import dash_bootstrap_components as dbc

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

def call_dashboard_loading_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "Start FERMO",
            id='call_dashboard_loading',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])


loading = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('FERMO: loading mode'),
                ],
            id="loading_row_1_col_1",
            width=12,
            ),
        ],
    id="loading_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for a brief par on how the loading mode works'),
                ],
            id="loading_row_2_col_1",
            width=12,
            ),
        ],
    id="loading_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for files to upload'),

                ],
            id="loading_row_3_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                ],
            id="loading_row_3_col_2",
            width=6,
            ),
        ],
    id="loading_row_3",
    ),
    ###fourth row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for start button'),
                call_dashboard_loading_button(),
                ],
            id="loading_row_4_col_1",
            width=12,
            ),
        ],
    id="loading_row_4",
    ),
    ])



