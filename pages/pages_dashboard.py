from dash import Dash, html, dcc, dash_table
# ~ from dash import Input, Output, callback, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd

#LOCAL MODULES

from variables import (
    style_data_table,
    style_data_cond_table,
    style_header_table,
    color_dict,
    feature_info_dict,
    load_cytoscape_attributes,
    info_node_dict,
    info_edge_dict)


##########
#VARIABLES
##########

feature_info_df = pd.DataFrame(feature_info_dict)
info_node_df = pd.DataFrame(info_node_dict)
info_edge_df = pd.DataFrame(info_edge_dict)



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









##########
#PAGE
##########

dashboard = html.Div([
    dbc.Row([
        #top left: sample names + scores
        dbc.Col([
            ####STORAGE####
            html.Div([
                dcc.Store(id='storage_feature_dicts'),
                dcc.Store(id='storage_samples_JSON'),
                dcc.Store(id='storage_sample_stats'),
                dcc.Store(id='threshold_values'),
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
                                'Specificity score',
                                'Total',
                                'Non-blank',
                                'Over cutoff',]
                            ],
                        style_as_list_view=True,
                        style_data=style_data_table,
                        style_data_conditional=style_data_cond_table,
                        style_header=style_header_table,
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
                # ~ html.Div(dcc.Graph(id='chromat_out')),
                # ~ html.Div(dcc.Graph(id='chromat_clique_out')),
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
                html.Div("Relative intensity: "),
                html.Div(call_threshold_inp('rel_intensity_threshold')),
                html.Div("Convolutedness: "),
                html.Div(call_threshold_inp('convolutedness_threshold')),
                html.Div("Bioactivity: "),
                html.Div(call_threshold_inp('bioactivity_threshold')),
                html.Div("Novelty: "),
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
                # ~ dbc.Button(
                    # ~ "Export peak table of selected sample (.csv)",
                    # ~ id='button_peak_table',
                    # ~ n_clicks=0,
                    # ~ ),
                # ~ dcc.Download(id="download_peak_table"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                # ~ dbc.Button(
                    # ~ "Export peak tables of all samples (.csv)",
                    # ~ id='button_all_peak_table',
                    # ~ n_clicks=0,
                    # ~ ),
                # ~ dcc.Download(id="download_all_peak_table"),
                ]),
            html.Div(style={'margin-top' : '10px',}),
            html.Div([
                # ~ dbc.Button(
                    # ~ "Export all feature as table(.csv)",
                    # ~ id='button_all_features_table',
                    # ~ n_clicks=0,
                    # ~ ),
                # ~ dcc.Download(id="download_all_features_table"),
                ]),
            ],
            id="dashboard_row_2_col_1",
            width=2,
        ),
        #bottom second: spectrum similarity network
        dbc.Col([
            html.Div(
                # ~ cyto.Cytoscape(
                    # ~ id='cytoscape',
                    # ~ layout={'name': 'cose'},
                    # ~ stylesheet=stylesheet_cytoscape,
                    # ~ style={'width': '100%', 'height': '30vh'},
                    # ~ ),
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
                # ~ dash_table.DataTable(
                    # ~ id='click-nodedata-output',
                    # ~ columns=[
                        # ~ {"name": i, "id": i, 'presentation': 'markdown'} 
                        # ~ for i in info_node_df.columns
                    # ~ ],
                    # ~ markdown_options={"html": True},
                    # ~ style_as_list_view=True,
                    # ~ style_data=style_data_table,
                    # ~ style_data_conditional=style_data_cond_table,
                    # ~ style_header=style_header_table,
                    # ~ ),
                # ~ style={
                    # ~ 'display': 'inline-block', 
                    # ~ 'width': '49%',
                    # ~ 'float': 'left'},
                ),
            html.Div(
                # ~ dash_table.DataTable(
                    # ~ id='click-edgedata-output',
                    # ~ columns=[
                        # ~ {"name": i, "id": i, 'presentation': 'markdown'} 
                        # ~ for i in info_edge_df.columns
                    # ~ ],
                    # ~ markdown_options={"html": True},
                    # ~ style_as_list_view=True,
                    # ~ style_data=style_data_table,
                    # ~ style_data_conditional=style_data_cond_table,
                    # ~ style_header=style_header_table,
                    # ~ ),
                # ~ style={
                    # ~ 'display': 'inline-block', 
                    # ~ 'width': '49%',
                    # ~ 'float': 'left'},
                ),
            ],
            id="dashboard_row_2_col_2",
            width=4,
            ),
        #bottom third: mini-chromatograms, sample overview
        dbc.Col([
            html.H3(id='title_mini_chrom',),
            # ~ html.Div(
                # ~ dcc.Graph(id='mini-chromatograms',),
                # ~ style={
                    # ~ 'width': '100%', 
                    # 'height': '70vh', #leave switched off
                    # ~ 'display': 'inline-block',
                    # ~ 'overflow': 'scroll',
                    # ~ },
                # ~ ),
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

