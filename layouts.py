from dash import html, dcc
import dash_bootstrap_components as dbc



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
        dbc.Col([
                
            ],
            id="landing_row_1_col_1",
            width=12,
            ),
        ],
    id="landing_row_1",
    ),
    ###second row###
    dbc.Row([
        dbc.Col([
                html.Div('landing_row_2_col_1'),
            ],
            id="landing_row_2_col_1",
            width=6,
            ),
        dbc.Col([
                html.Div('landing_row_2_col_'),
            ],
            id="landing_row_2_col_2",
            width=6,
            ),
        ],
    id="landing_row_2",
    ),
    ###third row###
    dbc.Row([
        dbc.Col([
                html.Div([
                    dbc.Button(
                        "Start FERMO!",
                        id='start_button',
                        color="primary",
                        n_clicks=0,
                        ),
                    ],
                    className="d-grid gap-2 col-6 mx-auto",
                ),
            ],
            id="landing_row_3_col_1",
            width=12,
            ),
        ],
    id="landing_row_3",
    ),
])
    
    
    
    
    # ~ #Row 1 : Header
    # ~ get_header(),
    # ~ #Row 2 : Nav bar
    # ~ get_navbar("images"),

    # ~ get_uploads_images(),

    # ~ # hidden signal value
    # ~ dcc.Store(id='signal_image'),
    
dashboard_page = html.Div([
    
    html.Div('Dashboard page'),
    # ~ html.Div(id='params_loading'),
    
    
    # ~ #Row 1 : Header
    # ~ get_header(),
    # ~ #Row 2 : Nav bar
    # ~ get_navbar("images"),

    # ~ get_uploads_images(),

    # ~ # hidden signal value
    # ~ dcc.Store(id='signal_image'),
    
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
