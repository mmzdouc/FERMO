from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

from variables import (
    style_data_table,
    style_data_cond_table,
    style_header_table,)

def call_loading_intro_text():
    '''Introduction text for loading page'''
    return html.Div([
        dcc.Markdown('''On this page, you can load **FERMO session files** in the **.json-format**. Reloading is very fast, since time-consuming computation steps are omitted. However, the parameters set during initial computation cannot be altered anymore.
            '''),
        dcc.Markdown('''To upload a **FERMO session file**, click the button with the name **'Upload FERMO Session File'** on the left side of the page. A message will appear to inform you about the outcome. 
            '''),
        dcc.Markdown('''If successful, session file metadata will be shown in the table on the right side of the window, including the time, date, and version of FERMO during creation, the names of the files used for processing, and the used parameter settings. 
            '''),
        dcc.Markdown('''After loading your data, click the button 'Start FERMO Dashboard' to go to the dashboard view.
            '''),
        ],
        style={
        'line-height' : '1.5',
        'text-align' : 'justify',
        }
    )

def call_session_upload():
    '''Call the session upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load FERMO Session File (*.json)',
                        id="upload-session-tooltip",
                        className="button_small_class",
                        ),
                    id='upload-session'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Load a previously created FERMO session file.
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-session-tooltip",
                    ),
                ]),
        ])

def call_dashboard_loading_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "Start FERMO Dashboard",
            id='call_dashboard_loading',
            n_clicks=0,
            className="button_general_class",
            style={'width' : '100%',}
            ),
        ],
        style={'margin' : 'auto','width' : '50%',},
        )



loading = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col(
            html.Div([
                ###STORAGE###
                dcc.Store(id='upload_session_storage'),
                #############
                html.H2('Restart session (loading mode)'),
                call_loading_intro_text(),
                html.Div(style={'margin-top' : '100px'}),
                html.Hr(),
                html.Div(style={'margin-top' : '15px'}),
                call_session_upload(),
                html.Div(id='upload_session_output',
                    style={
                        'margin-top' : '10px', 
                        'color' : 'red',
                        'font-weight' : 'bold',
                        }
                    ),
                ],
                style={
                        'margin-left':'30px',
                        'margin-top':'30px',
                        },
                ),
            id="loading_row_1_col_1",
            width=6,
            ),
        dbc.Col(
            html.Div(
                dash_table.DataTable(
                    id='upload_session_table',
                    columns=[
                        {"name": i, "id": i,'presentation': 'markdown'}
                        for i in ['Attribute','Description']],
                    markdown_options={"html": True},
                    style_cell={'textAlign': 'left'},
                    style_as_list_view=True,
                    style_data=style_data_table,
                    style_data_conditional=style_data_cond_table,
                    style_header=style_header_table,
                ),
                style={
                    'margin-top':'35px',
                    'margin-left':'30px',
                    'display': 'inline-block',
                    'width': '60%',
                    },
                ),
            id="loading_row_1_col_2",
            width=6,
            ),
        ],
    id="loading_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div(style={'margin-top' : '10px'}),
                call_dashboard_loading_button(),
                #Helper function
                html.Div(
                    id='loading_start_cache',
                    style={
                        'margin' : 'auto',
                        'width' : '50%',
                        'text-align' : 'center',
                        'font-weight' : 'bold',
                        'font-size' : '20px', 
                        },
                    )
                ],
            id="loading_row_2_col_1",
            width=12,
            ),
        ],
    id="loading_row_2",
    ),
])



