from dash import html, dcc
import dash_bootstrap_components as dbc

def call_processing_intro_text():
    '''Introduction text for processing page'''
    return html.Div([
        html.Div('''On this page, you can process your data with FERMO. The minimum requirements are:'''),
        dcc.Markdown('''
            * a **peaktable** containing general data on features (in the **'_quant_full.csv'** format created by **MZmine3**)
            * a **.mgf-file** containing **MS²** data (created together with peaktable by **MZmine3**)
        '''),
        html.Div('''Optionally, you can provide:'''),
        dcc.Markdown('''
            * **quantitative biological data** on samples (as .csv-file)
            * **group metadata** of samples (as .csv-file)
            * a **spectral library** (as .mgf-file)
        '''),
        dcc.Markdown('''On the left side of the page, you can **load input files** into FERMO. On the right,you can **adjust processing parameters**.
        '''),
        dcc.Markdown('''**Attention:** if you want to have your features annotated, switch **MS2Query** to **ON**. This will increase calculation time significantly.
        '''),
        dcc.Markdown('''You can find more information on [input data formats](https://github.com/mmzdouc/FERMO/wiki/Input-data-formats) and [parameter settings](https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page) in the FERMO Wiki.
        '''),
        dcc.Markdown('''You can start the analysis by clicking the **'Start FERMO'** button at the bottom of the page.
            '''),
        ],
    style={
    'line-height' : '1.5',
    'text-align' : 'justify',
    })

def call_dashboard_processing_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "Start FERMO",
            id='call_dashboard_processing',
            n_clicks=0,
            class_name="button_general_class",
            style={'width' : '100%',}
            ),
        ],
        style={'margin' : 'auto','width' : '50%',}
        )

def call_mass_dev_inp():
    '''Call estimated mass deviation input'''
    return html.Div([
        html.Div([
            '''
            Mass deviation:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="mass_dev_inp_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''Estimated mass deviation of your data in ppm. Used as precision threshold during different calculation steps (e.g. ion adduct calculation). For more information, click this info-button.
                    ''',
                    ),
                placement='right',
                className='info_dot_tooltip',
                target="mass_dev_inp_tooltip",
            ),
        dbc.Input(
            id='mass_dev_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=20, 
            min=0,
            step=1,
            style={'width' : '30%'},
            ),
        ])

def call_min_ms2_inpt():
    '''Call minimal nr ms2 fragments input field'''
    return html.Div([
        html.Div([ 
            '''Min fragments per MS² spectrum:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="min_ms2_inpt_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Quality control parameter. MS² spectra that do not exceed the minimum number of fragments are discarded and the feature is considered MS¹ only. Set this parameter to '0' if all spectra should be retained. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="min_ms2_inpt_tooltip",
            ),
        dbc.Input(
            id='min_ms2_inpt',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=8, 
            min=0,
            step=1,
            style={'width' : '30%'},
            ),
        ])

def call_bioact_fact_inp():
    '''Call the bioactivity factor input field'''
    return html.Div([
        html.Div([ 
            '''QuantData Factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="bioact_fact_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Only used if quantitative biological data was provided. If a feature was detected in samples with and without associated biological measurement, the fold difference between the lowest feature intensity from the sample with the lowest measurement and the highest feature intensity across inactive samples must be higher than the QuantData factor to still consider the feature associated to the measurement. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="bioact_fact_tooltip",
            ),
        dbc.Input(
            id='bioact_fact_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            step=1,
            style={'width' : '30%'},
            ),
        ])

def call_column_ret_fact_inp():
    '''Call the column retention factor input field '''
    return html.Div([
        html.Div([ 
            '''Blank factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="column_ret_fact_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Only used if group metadata was provided. If a feature was detected in both samples and blanks, the fold difference between the average intensity across samples and the average intensity across blanks must be higher than the blank factor to not consider the feature as blank-associated. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="column_ret_fact_tooltip",
            ),
        dbc.Input(
            id='column_ret_fact_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            step=1,
            style={'width' : '30%'},
            ),
        ])

def call_ms2query_toggle():
    '''Call toggle for ms2query switch'''
    return html.Div([
        html.Div([
            '''MS2Query:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="ms2query_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''Toggle to switch MS2Query annotation on or off. MS2Query is computationally costly and should be ideally run after parameter finding. For more information, click this info-button.
                    ''',
                    ),
                placement='right',
                className='info_dot_tooltip',
                target="ms2query_tooltip",
            ),
        html.Div(style={'margin-top' : '5px'}),
        dcc.RadioItems(
            options=[
                {
                "label": 'ON',
                "value": True,
                },
                {
                "label": 'OFF',
                "value": False,
                },
            ], 
            value=False,
            id='ms2query_toggle_input',
            inline=False,
            )
        ])


def call_spectral_sim_network_toggle():
    '''Call toggle for spectral similarity switch'''
    return html.Div([
        html.Div([
            '''Spectral similarity networking algorithm:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spectral_sim_network_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''Toggle to switch between different spectral 
                    similarity calculation algorithms. Modified cosine
                    is used most often. MS2DeepScore is a deep learning
                    based algorithm. For more information, click this
                    info-button. 
                    ''',
                    ),
                placement='right',
                className='info_dot_tooltip',
                target="spectral_sim_network_tooltip",
            ),
        html.Div(style={'margin-top' : '5px'}),
        dcc.RadioItems(
            options=[
                {
                "label": 'Modified cosine',
                "value": 'modified_cosine',
                },
                {
                "label": 'MS2DeepScore',
                "value": 'ms2deepscore',
                },
            ], 
            value='modified_cosine',
            id='spec_sim_net_alg_toggle_input',
            inline=False,
            )
        ])

def call_spec_sim_tol_inp():
    '''Call the spectrum similarity tolerance input field '''
    return html.Div([
        html.Div([ 
            '''Fragment similarity tolerance:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_tol_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Tolerance in m/z used in MS² spectra fragment comparison. Two fragments will be considered a match if their difference is less then or equal to the m/z tolerance. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_tol_tooltip",
            ),
        dbc.Input(
            id='spec_sim_tol_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0.1, 
            min=0,
            step=0.01,
            style={'width' : '30%'},
            ),
        ])

def call_spec_sim_score_cutoff_inp():
    '''Call the spectrum similarity score cutoff input field '''
    return html.Div([
        html.Div([ 
            '''
            Spectrum similarity score cutoff:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_score_cutoff_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Score cutoff used in the evaluation of modified cosine scores between MS2 spectra. Two spectra will be considered related only if their score exceeds the cutoff threshold. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_score_cutoff_tooltip",
            ),
        dbc.Input(
            id='spec_sim_score_cutoff_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0.8, 
            min=0,
            max=1,
            step=0.01,
            style={'width' : '30%'},
            ),
        ])

def call_spec_sim_max_links_inp():
    '''Call the spectrum similarity maximal links input field '''
    return html.Div([
        html.Div([ 
            '''
            Max spectral links:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_max_links_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Maximal number of links to other nodes, per node. Makes spectral similarity network less convoluted since it restricts the number of links between nodes to the highest n ones. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_max_links_tooltip",
            ),
        dbc.Input(
            id='spec_sim_max_links_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=10, 
            min=0,
            max=10,
            step=1,
            style={'width' : '30%'},
            ),
        ])

def call_spec_sim_min_match_inp():
    '''Call the spectrum similarity minimal matched peaks input field '''
    return html.Div([
        html.Div([ 
            '''Min matched peaks:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_min_match_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''In spectrum similarity matching, the minimum number of peaks that have to be matched between two spectra to be considered a match. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="spec_sim_min_match_tooltip",
            ),
        dbc.Input(
            id='spec_sim_min_match_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=8, 
            min=0,
            step=1,
            style={'width' : '30%'},
            ),
        ])


def call_rel_intens_filter_range_inp():
    '''Call the relative intensity filter range input field '''
    return html.Div([
        html.Div([ 
            '''Relative intensity filter:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="rel_intens_filter_range_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Filter to remove features with relative intensity 
                outside of the selected range from the analysis. This can
                be used to reduce low-intensity features to speed up 
                MS2Query annotation, or to remove all-dominating features, such as solvent peaks. For more information, click this info-button.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="rel_intens_filter_range_tooltip",
            ),
        html.Div([
            dcc.RangeSlider(
                id='relative_intensity_filter_range',
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
                ),
            ],
            style={'width' : '30%'},
            ),
        ])


def call_ms2query_blank_annot_toggle():
    '''Call toggle for ms2query blank features switch'''
    return html.Div([
        html.Div([
            '''MS2Query - annotate features from blanks?
            ''',
            html.A(
                html.Div(
                    "?",
                    id="ms2query_blank_annot_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''Toggle to switch on annotation of blank-associated
                    features by MS2Query. This can give additional 
                    information, but also leads to an increase in 
                    computation time, since there are more features to 
                    process.
                    ''',
                    ),
                placement='right',
                className='info_dot_tooltip',
                target="ms2query_blank_annot_tooltip",
            ),
        html.Div(style={'margin-top' : '5px'}),
        dcc.RadioItems(
            options=[
                {
                "label": 'ON',
                "value": True,
                },
                {
                "label": 'OFF',
                "value": False,
                },
            ], 
            value=False,
            id='ms2query_blank_annotation',
            inline=False,
            )
        ])

def call_bioact_type_dd():
    '''Call dropdown menu for bioactivity data specification'''
    return html.Div([
        html.Div([ 
            '''
            Specify format of quantitative biological data:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="call_bioact_type_tooltip",
                    className="info_dot"
                    ),
                href='https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''Accepts two formats: concentration and percentage (positive numbers only). For concentrations, the lowest value will be considered the highest activity. For percentage, the highest value will be considered the highest activity.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_bioact_type_tooltip",
            ),
        html.Div(
        dcc.Dropdown(
            options=[
               {'label': 'Concentration (i.e. lowest value = highest activity)', 'value': 'conc'},
               {'label': 'Percentage (i.e. highest value = highest activity)', 'value': 'perc'},
               ],
            value=None,
            id='bioact_type',
            style={'width' : '100%'}
            ),
            style={'width' : '30%'}
        )
        ])

def call_peaktable_upload():
    '''Call the peaktable upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load peaktable (*_quant_full.csv)',
                        id="upload-peaktable-tooltip",
                        className="button_small_class",
                        ),
                    id='processing-upload-peaktable'),
                dbc.Tooltip(
                    html.Div(
                        ''' Reads a MZmine3 style peaktable with the  '_quant_full.csv' suffix (exported in the FULL/ALL mode). For more information on the format, see the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-peaktable-tooltip",
                    ),
                ]),
        ])

def call_mgf_upload():
    '''Call the mgf upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load the MS/MS file (*.mgf)',
                        id="upload-mgf-tooltip",
                        className="button_small_class",
                        ),
                    id='processing-upload-mgf'),
                dbc.Tooltip(
                    html.Div(
                        ''' Reads a MZmine3 style .mgf-file containing tandem mass (MS/MS) spectra, accompanying the peaktable. Generated through MZmine3 export. For more information on the format, see the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-mgf-tooltip",
                    ),
                ]),
        ])

def call_bioactiv_upload():
    '''Call the bioactivity upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load quantitative biological data (*.csv)',
                        id="upload-bioactiv-tooltip",
                        className="button_small_class",
                        ),
                    id='upload-bioactiv'),
                dbc.Tooltip(
                    html.Div(
                        '''Quantitative biological data file in .csv format. For more information on the format, see the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-bioactiv-tooltip",
                    ),
                ]),
        ])

def call_metadata_upload():
    '''Call the metadata upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load group metadata table (*.csv)',
                        id="upload-metadata-tooltip",
                        className="button_small_class",
                        ),
                    id='upload-metadata'),
                dbc.Tooltip(
                    html.Div(
                        '''Metadata annotation file in .csv format. For more information on the format, see the documentation. 
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-metadata-tooltip",
                    ),
                ]),
        ])

def call_userlib_upload():
    '''Call the user spectral library upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Load spectral library (*.mgf)',
                        id="upload-userlib-tooltip",
                        className="button_small_class",
                        ),
                    id='upload-userlib'),
                dbc.Tooltip(
                    html.Div(
                        '''Reads a user-provided spectral library in the .mgf-format. For more information on the format, see the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-userlib-tooltip",
                    ),
                ]),
        ])


processing = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col(
            html.Div([
                html.H2('Processing mode (peaktable processing)'),
                call_processing_intro_text(),
                html.Div(style={'margin-top' : '30px'}),
                html.Hr(),
                #PEAKTABLE UPLOAD FIELD
                html.Div(style={'margin-top' : '15px'}),
                call_peaktable_upload(),
                html.Div(
                    id='upload-peaktable-output',
                    style={
                        'color' : 'red',
                        'font-weight' : 'bold',
                        'margin-top' : '5px', 
                        },
                    ),
                html.Div(style={'margin-top' : '15px'}),
                #MGF UPLOAD FIELD
                call_mgf_upload(),
                html.Div(
                    id='upload-mgf-output',
                    style={
                        'color' : 'red',
                        'font-weight' : 'bold',
                        'margin-top' : '5px', 
                        },
                    ),
                html.Div(style={'margin-top' : '15px'}),
                #BIOACTIVITY UPLOAD FIELD
                call_bioact_type_dd(),
                html.Div(style={'margin-top' : '5px'}),
                call_bioactiv_upload(),
                html.Div(
                    id='upload-bioactiv-output',
                    style={
                        'font-weight' : 'bold',
                        'margin-top' : '5px', 
                        },
                    ),
                html.Div(style={'margin-top' : '15px'}),
                #METADATA UPLOAD FIELD
                call_metadata_upload(),
                html.Div(
                    id='upload-metadata-output',
                    style={
                        'font-weight' : 'bold',
                        'margin-top' : '5px', 
                        },
                    ),
                html.Div(style={'margin-top' : '15px'}),
                #USER LIBRARY UPLOAD FIELD
                call_userlib_upload(),
                html.Div(
                    id='upload-userlib-output',
                    style={
                        'font-weight' : 'bold',
                        'margin-top' : '5px', 
                        },
                    ),
            ],
            style={
                'margin-left':'30px',
                'margin-top':'30px',
                },
            
            ),
            id="processing_row_1_col_1",
            width=7,
            ),
        #second column#
        dbc.Col(
            html.Div([
                html.H4('General parameters'),
                html.Div(style={'margin-top' : '10px'}),
                call_mass_dev_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_min_ms2_inpt(),
                html.Div(style={'margin-top' : '10px'}),
                call_bioact_fact_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_column_ret_fact_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_rel_intens_filter_range_inp(),
                html.Div(style={'margin-top' : '20px'}),
                html.H4('Networking and annotation parameters'),
                html.Div(style={'margin-top' : '10px'}),
                call_ms2query_toggle(),
                html.Div(style={'margin-top' : '10px'}),
                call_ms2query_blank_annot_toggle(),
                html.Div(style={'margin-top' : '10px'}),
                call_spectral_sim_network_toggle(),
                html.Div(style={'margin-top' : '10px'}),
                call_spec_sim_tol_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_spec_sim_score_cutoff_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_spec_sim_max_links_inp(),
                html.Div(style={'margin-top' : '10px'}),
                call_spec_sim_min_match_inp(),
            ],
            style={
                'margin-left':'80px',
                'margin-top':'80px',
                },
            ),
            id="processing_row_1_col_2",
            width=5,
            ),
        ],
    id="processing_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div(style={'margin-top' : '10px'}),
                call_dashboard_processing_button(),
                ###STORAGE###
                #Helper function
                html.Div(id='store_bioact_type'),
                #Parameter storage
                dcc.Store(id='out_params_assignment'),
                #File storage
                dcc.Store(id='upload_peaktable_store'),
                dcc.Store(id='upload_mgf_store'),
                dcc.Store(id='upload_bioactiv_store'),
                dcc.Store(id='upload_metadata_store'),
                dcc.Store(id='upload_userlib_store'),
                dcc.Store(id='uploaded_files_store'),
                html.Div(
                    id='processing_start_cache',
                    style={
                        'margin' : 'auto',
                        'width' : '50%',
                        'text-align' : 'center',
                        'font-weight' : 'bold',
                        'font-size' : '20px', 
                        }
                    ),
                ],
            id="processing_row_2_col_1",
            width=12,
            ),
        ],
    id="processing_row_2",
    ),
    ])









