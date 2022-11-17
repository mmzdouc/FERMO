from dash import Dash, html, dcc, dash_table
# ~ from dash import Input, Output, callback, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import dash_cytoscape as cyto

#LOCAL MODULES



##########
#VARIABLES
##########

#redo this part - not all dicts needed (maybe not even one!)
from app_utils.variables import (
    style_data_table,
    style_data_cond_table,
    style_header_table,
    color_dict,
    stylesheet_cytoscape,)

##########
#FUNCTIONS
##########

def call_legend_element(
    text,
    background_color,
    border_color,
    ):
    '''Generate legend element'''
    return html.Div([
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': background_color,
                    'border-color' : border_color,
                    },
                ),
            text,
            ]),
        ],
    style={
        'font-size': '16px',
        'display' : 'inline-block',
        'margin-right': '10px',
        },
    )

def call_legend_central_chrom():
    '''Generate legend for central chromatogram'''
    return html.Div([
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_green'],
                    'border-color' : color_dict['green'],},
                ),
            'Over cutoff',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_cyan'],
                    'border-color' : color_dict['cyan'],},
                ),
            'Below cutoff',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': 'white',
                    'border-color' : color_dict['purple'],},
                ),
            'Unique to sample',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': 'white',
                    'border-color' : color_dict['black'],},
                ),
            'Unique to group',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_yellow'],
                    'border-color' : color_dict['yellow'],},
                ),
            'Blank + MS1',
            ]),
        ],
    style={
        'font-size': '16px',
        },
    )

def call_legend_clique_chrom():
    '''Generate legend for clique chromatogram'''
    return html.Div([
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_blue'],
                    'border-color' : color_dict['blue'],},
                ),
            'Selected feature',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_red'],
                    'border-color' : color_dict['red'],},
                ),
            'Members of same molecular network',
            ]),
        ],
    style={
        'font-size': '16px',
        },
    )

def call_threshold_inp(name):
    '''Set parameters of dash dcc.Input field'''
    return dcc.Input(
        id=name, 
        value=0.0, 
        debounce=True,
        type='number',
        inputMode='numeric',
        min=0.0,
        max=1.0,
        step=0.01,)

def call_rel_int_title():
    '''Relative intensity factor title + info button'''
    return html.Div([
        html.Div([ 
            "Relative intensity: ",
            html.A(
                html.Div(
                    "?",
                    id="call_rel_int_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter peaks for relative intensity. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_rel_int_title_tooltip",
            ),
        ])

def call_convolutedness_title():
    '''Convolutedness factor title + info button'''
    return html.Div([
        html.Div([ 
            "Convolutedness score: ",
            html.A(
                html.Div(
                    "?",
                    id="call_convolutedness_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for peaks without collisions with other peaks (except adduct and isotope peaks). The higher the value, the less peak collision is allowed. '0' ignores collision, '0.5' allows overlap of 50% of peak with other peaks, '1' only selects peaks with no overlaps. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_convolutedness_title_tooltip",
            ),
        ])

def call_bioactivity_title():
    '''Bioactivity factor title + info button'''
    return html.Div([
        html.Div([ 
            "Bioactivity score: ",
            html.A(
                html.Div(
                    "?",
                    id="call_bioactivity_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for bioactivity-associated features (if bioactivity table was provided). A value >= 0.1 selects any putatively putatively bioactive feature. Values between 0.1 and 1 can be used to differentiate features coming from samples with lower or higher bioactivity. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_bioactivity_title_tooltip",
            ),
        ])

def call_novelty_title():
    '''Novelty factor title + info button'''
    return html.Div([
        html.Div([ 
            "Novelty score: ",
            html.A(
                html.Div(
                    "?",
                    id="call_novelty_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for putatively novel (unknown) features (if MS2Query was active and/or a spectral library was provided). A value of '0' would select all features, while a value of '1' would select only features that are most likely unknown. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_novelty_title_tooltip",
            ),
        ])



##########
#PAGE
##########

dashboard = html.Div([
    dbc.Row([
        #top left: sample names + scores
        dbc.Col([
            ####STORAGE####
            html.Div([
                dcc.Store(id='threshold_values'),
                dcc.Store(id='samples_subsets'),
                dcc.Store(id='sample_list'),
                dcc.Store(id='storage_active_sample'),
                dcc.Store(id='storage_active_feature_index'), 
                dcc.Store(id='storage_active_feature_id'), 
                ]),
            ###############
                html.Div(
                    dash_table.DataTable(
                        id='table_sample_names',
                        columns=[
                            {"name": i, "id": i} 
                            for i in [
                                'Filename',
                                'Group',
                                'Diversity score',
                                'Spec score',
                                'Total',
                                'Non-blank',
                                'Over cutoff',]
                            ],
                        style_as_list_view=True,
                        style_data=style_data_table,
                        style_data_conditional=style_data_cond_table,
                        style_header=style_header_table,
                        tooltip_header={
                            'Diversity score' : 'Chemical diversity of sample. Nr of discrete spectral similarity cliques per sample, divided by total of cliques across all samples (excluding cliques from BLANKs).',
                            'Spec score' : 'Specificity score: Group-specific chemistry per sample. Nr of spectral similarity cliques specific to group the sample is in, divided by total nr of cliques in sample.'
                            },
                        tooltip_delay=0,
                        tooltip_duration=None,
                        ),
                    style={'display': 'inline-block'},
                ),
            ],
            id="dashboard_row_1_col_1",
            width=3,
            ),
        #top right: chromatogram view
        dbc.Col([
                html.H3(
                    id='title_central_chrom',
                    style={
                    'margin-top' : '10px',
                    'margin-left' : '25px',
                        }
                    ),
                html.Div([
                    html.Div(
                        dcc.Graph(id='chromat_out'),
                        style={
                        'display': 'inline-block', 
                        'width': '90%',
                        'float': 'left'},
                        ),
                    html.Div(
                        call_legend_central_chrom(),
                        style={
                        'display': 'inline-block', 
                        'width': '10%',
                        'float': 'left'},
                        ),
                    ]),
                html.Div([
                    html.Div(
                        dcc.Graph(id='chromat_clique_out'),
                        style={
                        'display': 'inline-block', 
                        'width': '90%',
                        'float': 'left'},
                        ),
                    html.Div(
                        call_legend_clique_chrom(),
                        style={
                        'display': 'inline-block', 
                        'width': '10%',
                        'float': 'left'},
                        ),
                    ]),
            ],
            id="dashboard_row_1_col_2",
            width=9,
            ),
        ],
    id="dashboard_row_1",
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("Set filters for cutoff and press enter.",
                    style={
                        'margin': '10px 5px 20px',
                        'font-size': '17px'},
                    ),
                call_novelty_title(),
                html.Div(call_threshold_inp('novelty_threshold')),
                call_bioactivity_title(),
                html.Div(call_threshold_inp('bioactivity_threshold')),
                call_convolutedness_title(),
                html.Div(call_threshold_inp('convolutedness_threshold')),
                call_rel_int_title(),
                html.Div(call_threshold_inp('rel_intensity_threshold')),
                ],
                style={
                    'margin-left': '10px',
                    'font-size': '17px',}
                ),
            html.Hr(
                style={
                    'margin-top' : '10px',
                    'margin-bottom' : '10px',
                    }
                ),
            html.Div([
                html.Div([
                    dbc.Button(
                        "Export peak table of selected sample (.csv)",
                        id='button_peak_table',
                        n_clicks=0,
                        className="button_small_class",
                        style={'width' : '100%',}
                        ),
                    ],
                style={'margin' : 'auto','width' : '100%',}
                ),
                dcc.Download(id="download_peak_table"),
                dcc.Download(id="download_peak_table_logging"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                html.Div([
                    dbc.Button(
                        "Export peak tables of all samples (.csv)",
                        id='button_all_peak_table',
                        n_clicks=0,
                        className="button_small_class",
                        style={'width' : '100%',}
                        ),
                    ],
                style={'margin' : 'auto','width' : '100%',}
                ),
                dcc.Download(id="download_all_peak_table"),
                dcc.Download(id="download_all_peak_table_logging"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                html.Div([
                    dbc.Button(
                        "Export all feature as table(.csv)",
                        id='button_all_features_table',
                        n_clicks=0,
                        className="button_small_class",
                        style={'width' : '100%',}
                        ),
                    ],
                style={'margin' : 'auto','width' : '100%',}
                ),
                dcc.Download(id="download_all_features_table"),
                dcc.Download(id="download_all_features_table_logging"),
                ]),
            html.Hr(
                style={
                    'margin-top' : '10px',
                    'margin-bottom' : '10px',
                    }
                ),
            html.Div([
                html.Div([
                    dbc.Button(
                        "Save FERMO session file (JSON)",
                        id='button_export_session',
                        n_clicks=0,
                        className="button_small_class",
                        style={
                            'width' : '100%',
                            'padding' : '15px',
                            'font-size' : '16px',
                            }
                        ),
                    ],
                style={'margin' : 'auto','width' : '100%',}
                ),
                dcc.Download(id="export_session_file"),
                ]),
            ],
            id="dashboard_row_2_col_1",
            width=2,
        ),
        #bottom second: spectrum similarity network
        dbc.Col([
            html.Div(
                cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'cose'},
                    stylesheet=stylesheet_cytoscape,
                    style={'width': '100%', 'height': '30vh'},
                    ),
                ),
            html.Div([
                call_legend_element(
                    'Selected Feature',
                    color_dict['blue'],
                    color_dict['blue'],
                    ),
                call_legend_element(
                    'Present in Sample',
                    color_dict['red'],
                    color_dict['red'],
                    ),
                call_legend_element(
                    'Other Samples',
                    color_dict['grey'],
                    color_dict['grey'],
                    ),
                ],
                style={
                    'margin-bottom': '5px', 
                    },
            ),
            html.Div([
                call_legend_element(
                    'Unique to sample',
                    'white',
                    color_dict['purple'],
                    ),
                call_legend_element(
                    'Unique to group',
                    'white',
                    color_dict['black'],
                    ),
                ],
                style={
                    'margin-bottom': '10px', 
                    },
            ),
            html.Div(
                dash_table.DataTable(
                    id='click-nodedata-output',
                    columns=[
                        {"name": i, "id": i, 'presentation': 'markdown'} 
                        for i in ['Node info', 'Description']
                    ],
                    markdown_options={"html": True},
                    style_as_list_view=True,
                    style_data=style_data_table,
                    style_data_conditional=style_data_cond_table,
                    style_header=style_header_table,
                    ),
                style={
                    'display': 'inline-block', 
                    'width': '49%',
                    'float': 'left'},
                ),
            html.Div(
                dash_table.DataTable(
                    id='click-edgedata-output',
                    columns=[
                        {"name": i, "id": i, 'presentation': 'markdown'} 
                        for i in ['Edge info', 'Description']
                    ],
                    markdown_options={"html": True},
                    style_as_list_view=True,
                    style_data=style_data_table,
                    style_data_conditional=style_data_cond_table,
                    style_header=style_header_table,
                    ),
                style={
                    'display': 'inline-block', 
                    'width': '49%',
                    'float': 'left'},
                ),
            ],
            id="dashboard_row_2_col_2",
            width=4,
            ),
        #bottom third: mini-chromatograms, sample overview
        dbc.Col([
            html.H3(id='title_mini_chrom',),
            html.Div(
                dcc.Graph(id='mini_chromatograms',),
                style={
                    'width': '100%', 
                    # ~ # 'height': '70vh', #leave switched off
                    'display': 'inline-block',
                    'overflow': 'scroll',
                    },
                ),
            ],
            id="dashboard_row_2_col_3",
            width=3,
            ),
        #bottom fourth: feature info table
        dbc.Col([
            html.Div(
                dash_table.DataTable(
                    id='featureinfo_out',
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
                    'display': 'inline-block',
                    'width': '100%',},
                ),
            ],
            id="dashboard_row_2_col_4",
            width=3,
            ),
        ],
    id="dashboard_row_2",
    ),
])

