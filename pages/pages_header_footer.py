from dash import html
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
