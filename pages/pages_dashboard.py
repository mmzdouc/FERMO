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
from variables import (
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
        'padding-top' : '50px',},
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
        'padding-top' : '170px',},
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
            "Relative intensity score: ",
            html.A(
                html.Div(
                    "?",
                    id="call_rel_int_title_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for feature intensity (height) relative to the most intense (highest) feature per sample. A value of 0 selects all features, a value of 1 only the most intense one. For more information, click this info-button to access the docs.
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
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for convolutedness (i.e. peak collisions) of each feature. Score represent proportion of feature not overlapping with other features (also detects various adducts and isotopic peaks and ignores overlaps between related features). For filtering, 0 would select all features, 0.5 would select features with at least 50% of retention time window not overlapping with any peaks, and 1 would only select features that are not overlapping with any other feature.For more information, click this info-button to access the docs.
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
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for associatedness to bioactivity of each feature. Only functional if a bioactivity table was provided by user. A feature is considered bioactive if 1) it has been detected only in samples that were designated as active; OR if 2) the minimum intensity across all bioactive samples is n times higher than the maximum intensity across all inactive samples, where n is a user-provided parameter with the name "Bioactivity factor". For filtering, any value greater than 0 selects all bioactivity-associated features. If multiple bioactive samples with different activity levels were designated, values between 0.1 and 1 can be used to differentiate features less or more likely to be bioactivity-associated. Keep in mind that a positive bioactivity score does not guarantee bioactivity of a compound. For more information, click this info-button to access the docs.
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
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for probability that feature is unknown, compared against external data. Indicates likeliness that the compound represented by the feature has not been described yet. Score calculated from results of MS2Query matching against a  spectral library containing approximately 300.000 compounds, and, if provided, from results of matching against a user-provided spectral library. For filtering, a score of 1 would indicate that the feature is most likely novel, while a score of 0 would indicate that the feature is most likely known. Keep in mind that the estimation of novelty is imperfect and dependent on external data provided. For more information, click this info-button to access the docs.
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
                            'Diversity score' : 'Number of different spectral similarity cliques per sample, divided by the total number of spectral similarity cliques across all samples. Indicates chemical diversity of sample.',
                            'Spec score' : 'Specificity score: Number of spectral similarity cliques unique to the sample and to the group this sample is in, divided by the total number of spectral similarity cliques across all samples. Indicates chemistry specific to sample/group.'
                            },
                        tooltip_delay=0,
                        tooltip_duration=None,
                        ),
                    style={'display': 'inline-block'},
                ),
            ],
            id="dashboard_row_1_col_1",
            width=2,
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
                html.Div(dcc.Graph(id='chromat_out')),
                html.Div(dcc.Graph(id='chromat_clique_out')),
            ],
            id="dashboard_row_1_col_2",
            width=9,
            ),
        #top_rightmost
        dbc.Col([
            call_legend_central_chrom(),
            call_legend_clique_chrom(),
            ],
            id="dashboard_row_1_col_3",
            width=1,
            ),
        ],
    id="dashboard_row_1",
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("Set threshold (0-1) and press enter.",
                    style={
                        'margin': '10px 5px 20px',
                        'font-size': '17px'},
                    ),
                call_rel_int_title(),
                html.Div(call_threshold_inp('rel_intensity_threshold')),
                call_convolutedness_title(),
                html.Div(call_threshold_inp('convolutedness_threshold')),
                call_bioactivity_title(),
                html.Div(call_threshold_inp('bioactivity_threshold')),
                call_novelty_title(),
                html.Div(call_threshold_inp('novelty_threshold')),
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
                dbc.Button(
                    "Export peak table of selected sample (.csv)",
                    id='button_peak_table',
                    n_clicks=0,
                    ),
                dcc.Download(id="download_peak_table"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                dbc.Button(
                    "Export peak tables of all samples (.csv)",
                    id='button_all_peak_table',
                    n_clicks=0,
                    ),
                dcc.Download(id="download_all_peak_table"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                dbc.Button(
                    "Export all feature as table(.csv)",
                    id='button_all_features_table',
                    n_clicks=0,
                    ),
                dcc.Download(id="download_all_features_table"),
                ]),
            html.Hr(
                style={
                    'margin-top' : '10px',
                    'margin-bottom' : '10px',
                    }
                ),
            html.Div([
                dbc.Button(
                    "Save FERMO session file (JSON)",
                    id='button_export_session',
                    n_clicks=0,
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

