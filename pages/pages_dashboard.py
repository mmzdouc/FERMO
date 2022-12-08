from dash import Dash, html, dcc, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import dash_cytoscape as cyto



##########
#VARIABLES
##########


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
            'Selected',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_cyan'],
                    'border-color' : color_dict['cyan'],},
                ),
            'Not selected',
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
            'Focused feature',
            ]),
        html.Div([
            html.Div(
                className="legend_rect",
                style={
                    'background-color': color_dict['light_red'],
                    'border-color' : color_dict['red'],},
                ),
            'Related (same molecular network)',
            ]),
        ],
    style={
        'font-size': '16px',
        },
    )


def call_rel_int_title():
    '''Relative intensity factor title + info button'''
    return html.Div([
        html.Div([ 
            "Relative intensity ",
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
                '''Filter features for relative intensity. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_rel_int_title_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )


def call_peak_collision_title():
    '''Peak collision title + info button'''
    return html.Div([
        html.Div([ 
            "Peak overlap (%) ",
            html.A(
                html.Div(
                    "?",
                    id="peak_collision_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter features for peak collisions. The higher the value, 
                the more of the peak is overlapping (colliding) with 
                another peak. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="peak_collision_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )



def call_adduct_title():
    '''Adduct/isotope title + info button'''
    return html.Div([
        html.Div([ 
            "Adduct/isotope search ",
            html.A(
                html.Div(
                    "?",
                    id="call_adduct_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for features with annotations as 
                adducts/isotopes. Filter uses regular expressions (POSIX ERE), and
                certain characters have special meaning. 
                For example, to select all annotations, use expression '.+'. For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_adduct_title_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_bioactivity_title():
    '''Bioactivity factor title + info button'''
    return html.Div([
        html.Div([ 
            "QuantData-associated ",
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
                '''Select features associated with quantitative biological data (if such data was provided). 'ON' selects any feature putatively associated with quantitative biological data. Click button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_bioactivity_title_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_novelty_title():
    '''Novelty factor title + info button'''
    return html.Div([
        html.Div([ 
            "Novelty score ",
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
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_annotation_search_title():
    '''Title for adduct search via regexp'''
    return html.Div([
        html.Div([ 
            "Annotation search ",
            html.A(
                html.Div(
                    "?",
                    id="call_annotation_search_title_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for features with annotation from library/MS2Query matching. Filter uses regular expressions (POSIX ERE), and
                certain characters have special meaning. 
                For example, to select all annotations, use expression '.+'. For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_annotation_search_title_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_feature_id_filter_name():
    '''Title for feature id search'''
    return html.Div([
        html.Div([ 
            "Feature ID search ",
            html.A(
                html.Div(
                    "?",
                    id="call_feature_id_filter_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for feature ID. Filters features
                for a single feature ID number. For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_feature_id_filter_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_clique_filter_name():
    '''Title for clique id search'''
    return html.Div([
        html.Div([ 
            "Spectral network ID search ",
            html.A(
                html.Div(
                    "?",
                    id="call_clique_filter_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for spectral similarity network ID.
                Filters for features in a specific spectral network (does
                not include blank features since they are deselected by
                default. For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_clique_filter_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )


def call_precursor_mz_filter_name():
    '''Title for precursor mz search'''
    return html.Div([
        html.Div([ 
            "Precursor m/z search ",
            html.A(
                html.Div(
                    "?",
                    id="call_precursor_mz_filter_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for feature precursor m/z. Filters features
                for a range of values. For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_precursor_mz_filter_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_visualization_selected_name():
    '''Title for visualization of selected features only'''
    return html.Div([
        html.Div([ 
            "Visualization of features ",
            html.A(
                html.Div(
                    "?",
                    id="call_visualization_selected_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Toggles visualization of features in chromatogram. 
                'ALL' shows all features, 'SELECTED', shows only the 
                currently selected features and discables non-selected 
                or blank features.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_visualization_selected_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )


def call_foldchange_search_name():
    '''Title for foldchange search'''
    return html.Div([
        html.Div([ 
            "Fold-changes filter ",
            html.A(
                html.Div(
                    "?",
                    id="call_foldchange_search_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for fold-changes of features between groups.
                Fold-changes between groups are calculated by pairwise
                division of average intensity between groups. 
                Only applicable if group metadata was provided.
                For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_foldchange_search_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_group_search_name():
    '''Title for group search in features'''
    return html.Div([
        html.Div([ 
            "Group filter (features) ",
            html.A(
                html.Div(
                    "?",
                    id="call_group_search_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for group metadata for individual
                features.
                Filter uses regular expressions (POSIX ERE), and
                certain characters have special meaning. 
                For example, to select multiple group annotations, 
                use expression 'group1|group2'. To exclude a specific
                group, use expression "^((?!groupname).)*$".
                For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_group_search_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_group_search_clique_name():
    '''Title for group search in cliques'''
    return html.Div([
        html.Div([ 
            "Group filter (networks) ",
            html.A(
                html.Div(
                    "?",
                    id="call_group_search_clique_name_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Scores-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter for group metadata for similarity networks.
                Filter uses regular expressions (POSIX ERE), and
                certain characters have special meaning. 
                For example, to select multiple group annotations, 
                use expression 'group1|group2'. To exclude a specific
                group, use expression "^((?!groupname).)*$".
                For more information,
                click the info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_group_search_clique_name_tooltip",
            ),
        ],
        style={'display': 'inline-block', 'width': '60%',},
        )

def call_rangeslider_inp(name):
    '''Set parameters of dash dcc.rangeslider field'''
    return html.Div([
        dcc.RangeSlider(
            id=name,
            min=0,
            max=1,
            marks=None,
            value=[0,1],
            tooltip={
                "placement": "bottom",
                "always_visible": True
                },
            allowCross=False,
            pushable=0,
            updatemode='mouseup',
            )],
            style={'display': 'inline-block', 'width': '60%',},
        )

def call_bioactivity_toggle(name):
    '''Call toggle for bioactivity'''
    return html.Div(dcc.RadioItems(
        options=[
            {
            "label": 'OFF',
            "value": 'OFF',
            },
            {
            "label": 'SPECIFICITY',
            "value": 'SPECIFICITY',
            },
            {
            "label": 'SPEC.+TREND',
            "value": 'SPEC.+TREND',
            },
        ], 
        value='OFF',
        id=name,
        inline=False,
        )
        )

def call_regexp_filter_str(name):
    '''Set text field for regex search'''
    return html.Div(dcc.Input(
        id=name, 
        value='', 
        debounce=True,
        placeholder='Regular expression search',
        type='text',
        style={'font-size' : '15px','width': '100%',},
        ),
        style={'width': '60%',},
        )

def call_int_filter_input(name, placeholder):
    '''Set int field filter'''
    return html.Div(dcc.Input(
        id=name, 
        value='', 
        debounce=True,
        placeholder=placeholder,
        min=0,
        step=1,
        type='number',
        style={'font-size' : '15px','width': '100%',},
        ),
        style={'width': '60%',},
        )

def call_float_precursor_inp(name, placeholder, value):
    '''Set float input field for m/z search'''
    return html.Div(dcc.Input(
        id=name, 
        value=value, 
        debounce=True,
        type='number',
        placeholder=placeholder,
        min=0.0,
        step=0.0001,
        style={'font-size' : '15px', 'width' : '100%'},
        ))

def call_selected_viz_toggle(name):
    '''Call toggle for visualization of selected features only'''
    return html.Div(dcc.RadioItems(
        options=[
            {
            "label": 'ALL',
            "value": 'ALL',
            },
            {
            "label": 'SELECTED',
            "value": 'SELECTED',
            },
            {
            "label": 'HIDDEN',
            "value": 'HIDDEN',
            },
        ], 
        value='ALL',
        id=name,
        inline=False,
        ))

def call_header_filter_column():
    '''Call div of header filter column'''
    return html.Div([
        html.Hr(style={
            'margin-top' : '10px',
            }),
        html.Div('Set filters for cutoff and press enter:',
            style={
                'font-size': '17px',
                'margin-left' : '10px',
                }
            ),
        html.Hr(style={
            'margin-top' : '10px',
            'margin-bottom' : '10px',
            }),
        ],
        style={
            'display' : 'inline-block',
            'width' : '75%',
            }
        )

def call_header_export():
    '''Call div of header export'''
    return html.Div([
        html.Hr(style={
            'margin-top' : '10px',
            }),
        html.Div('Export features as tables (.csv):',
            style={
                'font-size': '17px',
                'margin-left' : '10px',
                }
            ),
        html.Hr(style={
            'margin-top' : '10px',
            'margin-bottom' : '10px',
            }),
        ],
        style={
            'display' : 'inline-block',
            'width' : '75%',
            }
        )

def call_precursor_mz_filter_wrapper():
    '''Call div of precursor_mz_filter_wrapper '''
    return html.Div([
        html.Div(
            call_float_precursor_inp(
                'filter_precursor_min', 
                'min m/z', 
                0
                ),
            style={
                'width' : '49%',
                'display' : 'inline-block', 
                'float' : 'left', 
                },
            ),
        html.Div(
            call_float_precursor_inp(
                'filter_precursor_max', 
                'max m/z', 
                ''),
            style={
                'width' : '49%',
                'display' : 'inline-block', 
                'float' : 'right', },
            ),
        ],
        style={
            'display' : 'inline-block', 
            'margins' : 'auto',
            'width' : '60%'},
        )

def call_export_session_file_button():
    '''Call session file export button'''
    return html.Div([
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
        dcc.Download(id="export_session_file"),
        ],
        style={
            'margin' : 'auto',
            'margin-left' : '10px',
            'width' : '60%',
            'display' : 'inline-block',
            }
        )




def call_dd_menu_export():
    '''Call dropdown menu for feature info export'''
    return html.Div(
        dcc.Dropdown(
            options=[
               {'label': 'Peak table | selected sample, selected features', 'value': 'peak_sel_sam_sel_feat'},
               {'label': 'Peak table | selected sample, all features', 'value': 'peak_sel_sam_all_feat'},
               {'label': 'Peak table | all samples, selected features', 'value': 'peak_all_sam_sel_feat'},
               {'label': 'Peak table | all samples, all features', 'value': 'peak_all_sam_all_feat'},
               {'label': 'Feature table | selected features', 'value': 'feature_sel'},
               {'label': 'Feature table | all features', 'value': 'feature_all'},
               ],
            value=None,
            id='dd_export_type',
            style={'width' : '100%'}
            ),
            style={'width' : '60%', 'margin-left' : '10px',}
        )

def call_feature_export_button():
    '''Call peaktable/feature table export button'''
    return html.Div(
        html.Div([
            html.Div([
                dbc.Button(
                    "Export table",
                    id='feature_export_button',
                    n_clicks=0,
                    className="button_small_class",
                    style={'width' : '100%',}
                    ),
                ],
            ),
            dcc.Download(id="download_feature_export_button"),
            dcc.Download(id="download_feature_export_logging"),
            ]),
        style={
            'display' : 'inline-block',
            'margins' : 'auto',
            'margin-left' : '10px',
            'width' : '60%'},
        )

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
                dcc.Store(id='selected_viz_toggle_value'), 
                ]),
            ###############
                html.Div(style={'margin-top' : '10px'}),
                html.Div(
                    dash_table.DataTable(
                        id='table_general_stats',
                        columns=[
                            {"name": i, "id": i} 
                            for i in [
                                'Nr of samples',
                                'Nr of features',
                                'Selected features',
                                'Selected networks',
                                'Non-blank',
                                'Blank & MS1',
                                ]
                            ],
                        style_as_list_view=True,
                        style_data=style_data_table,
                        style_header=style_header_table,
                        ),
                ),
                html.Div(style={'margin-top' : '10px'}),
                html.Div(
                    dash_table.DataTable(
                        id='table_sample_names',
                        columns=[
                            {"name": i, "id": i} 
                            for i in [
                                'Filename',
                                'Group',
                                'Selected features',
                                'Selected networks',
                                'Diversity score',
                                'Spec score',
                                'Mean Novelty score',
                                'Total',
                                'Non-blank',
                                'Blank & MS1',
                                ]
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
                        'float': 'left',
                        'background-image' : f'''repeating-linear-gradient(
                            180deg, 
                            {color_dict['light_blue_0.15']}, 
                            {color_dict['light_blue_0.15']} 30px, 
                            {color_dict['light_blue_0.10']} 30px, 
                            {color_dict['light_blue_0.10']} 60px 
                            )''',
                        },
                        ),
                    html.Div(
                        call_legend_central_chrom(),
                        style={
                        'display': 'inline-block', 
                        'width': '10%',
                        'float': 'left'},
                        ),
                    ]),
                html.Div(style={
                    'margin-top' : '5px',
                    'display': 'inline-block',
                    'width': '100%',
                    'float': 'left',
                    }),
                html.Div([
                    html.Div(
                        dcc.Graph(id='chromat_clique_out'),
                        style={
                        'display': 'inline-block', 
                        'width': '90%',
                        'float': 'left',
                        'background-image' : f'''repeating-linear-gradient(
                            180deg, 
                            {color_dict['light_blue_0.15']}, 
                            {color_dict['light_blue_0.15']} 30px, 
                            {color_dict['light_blue_0.10']} 30px, 
                            {color_dict['light_blue_0.10']} 60px 
                            )''',
                        },
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
            html.Hr(
                style={
                    'margin-top' : '10px',
                    # ~ 'margin-bottom' : '10px',
                    'width' : '75%',
                    'display' : 'inline-block',
                    }
                ),
            call_export_session_file_button(),
            call_header_filter_column(),
            html.Div([
                call_visualization_selected_name(),
                call_selected_viz_toggle('selected_viz_toggle'),
                html.Div(style={'margin-top' : '5px'}),
                call_novelty_title(),
                call_rangeslider_inp('novelty_threshold'),
                html.Div(style={'margin-top' : '5px'}),
                call_rel_int_title(),
                call_rangeslider_inp('rel_intensity_threshold'),
                html.Div(style={'margin-top' : '5px'}),
                call_peak_collision_title(),
                call_rangeslider_inp('peak_overlap_threshold'),
                html.Div(style={'margin-top' : '5px'}),
                call_bioactivity_title(),
                call_bioactivity_toggle('bioactivity_threshold'),
                html.Div(style={'margin-top' : '5px'}),
                call_adduct_title(),
                call_regexp_filter_str('filter_adduct_isotopes'),
                html.Div(style={'margin-top' : '5px'}),
                call_annotation_search_title(),
                call_regexp_filter_str('filter_annotation'),
                html.Div(style={'margin-top' : '5px'}),
                call_feature_id_filter_name(),
                call_int_filter_input('filter_feature_id', 'Feature ID number'),
                html.Div(style={'margin-top' : '5px'}),
                call_clique_filter_name(),
                call_int_filter_input('filter_spectral_sim_netw', 'Network ID number'),
                html.Div(style={'margin-top' : '5px'}),
                call_foldchange_search_name(),
                call_int_filter_input('filter_fold_change', 'Search fold-change'),
                html.Div(style={'margin-top' : '5px'}),
                call_group_search_name(),
                call_regexp_filter_str('filter_group'),
                html.Div(style={'margin-top' : '5px'}),
                call_group_search_clique_name(),
                call_regexp_filter_str('filter_group_cliques'),
                html.Div(style={'margin-top' : '5px'}),
                call_precursor_mz_filter_name(),
                call_precursor_mz_filter_wrapper(),
                ],
                style={'margin-left': '10px','font-size': '17px',}
                ),
            call_header_export(),
            call_dd_menu_export(),
            html.Div(style={'margin-top' : '5px'}),
            call_feature_export_button(),
            html.Div(style={'margin-top' : '5px'}),
            ],
            id="dashboard_row_2_col_1",
            width=3,
        ),
        #bottom second: spectrum similarity network
        dbc.Col([
            html.Div(
                'Cytoscape view - spectral similarity networking',
                style={
                    'margin-bottom' : '10px', 
                    'font-size' : '18px',
                    'font-weight' : 'bold',
                    },
                ),
            html.Div(
                id='cytoscape_error_message', 
                style={
                    'margin-bottom' : '10px', 
                    'font-size' : '16px'
                    },
                ),
            html.Div(
                cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'cose'},
                    stylesheet=stylesheet_cytoscape,
                    style={
                        'width': '100%', 
                        'height': '30vh',
                        'border-style' : 'solid',
                        'border-width' : '2px',
                        'border-color' : color_dict['grey'],
                        },
                    ),
                ),
            html.Div([
                call_legend_element(
                    'Focused feature',
                    color_dict['blue'],
                    color_dict['blue'],
                    ),
                call_legend_element(
                    'Present in sample',
                    color_dict['red'],
                    color_dict['red'],
                    ),
                call_legend_element(
                    'Other samples',
                    color_dict['grey'],
                    color_dict['grey'],
                    ),
                ],
                style={
                    'margin-top': '10px', 
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
            html.Div(
                'Sample chromatograms',
                style={
                    'margin-bottom' : '10px', 
                    'font-size' : '18px',
                    'font-weight' : 'bold',
                    },
                ),
            html.Div(
                id='title_mini_chrom', 
                style={
                    'margin-bottom' : '10px', 
                    'font-size' : '16px'
                    },
                ),
            
            
            html.Div(
                id='mini_chromatograms',
                style={
                    'width': '100%', 
                    'display': 'inline-block',
                    'overflow': 'scroll',
                    },
                ),
            ],
            id="dashboard_row_2_col_3",
            width=2,
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

