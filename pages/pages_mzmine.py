from dash import html
import dash_bootstrap_components as dbc


def call_dashboard_mzmine_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "Start FERMO",
            id='call_dashboard_mzmine',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])

mzmine = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('FERMO: MZmine pre-processing mode'),
                ],
            id="mzmine_row_1_col_1",
            width=12,
            ),
        ],
    id="mzmine_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for a brief par on how the pre-processing mode works'),
                ],
            id="mzmine_row_2_col_1",
            width=12,
            ),
        ],
    id="mzmine_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for files to upload'),

                ],
            id="mzmine_row_3_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                html.Div('Placeholder for parameter settings'),
                ],
            id="mzmine_row_3_col_2",
            width=6,
            ),
        ],
    id="mzmine_row_3",
    ),
    ###fourth row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for start button'),
                call_dashboard_mzmine_button(),
                ],
            id="mzmine_row_4_col_1",
            width=12,
            ),
        ],
    id="mzmine_row_4",
    ),
    ])


