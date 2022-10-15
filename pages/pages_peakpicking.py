from dash import html
import dash_bootstrap_components as dbc


def call_dashboard_peakpicking_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "",
            # ~ id='call_dashboard_peakpicking',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            disabled=True,
            ),
        ])

peakpicking = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
                ],
            id="peakpicking_row_1_col_1",
            width=12,
            ),
        ],
    id="peakpicking_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                ],
            id="peakpicking_row_2_col_1",
            width=12,
            ),
        ],
    id="peakpicking_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                ],
            id="peakpicking_row_3_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                ],
            id="peakpicking_row_3_col_2",
            width=6,
            ),
        ],
    id="peakpicking_row_3",
    ),
    ###fourth row###
    dbc.Row([
        #first column#
        dbc.Col([
                call_dashboard_peakpicking_button(),
                html.Div(
                    # ~ id='peakpicking_start_cache',
                    style={
                        'text-align' : 'center',
                    })
                ],
            id="peakpicking_row_4_col_1",
            width=12,
            ),
        ],
    id="peakpicking_row_4",
    ),
    ])


