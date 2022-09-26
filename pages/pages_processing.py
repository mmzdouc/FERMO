from dash import html, dcc
import dash_bootstrap_components as dbc

def call_dashboard_processing_button():
    '''Create button that initializes FERMO calc and redir to dashboard'''
    return html.Div([
        dbc.Button(
            "Start FERMO",
            id='call_dashboard_processing',
            n_clicks=0,
            className="d-grid gap-2 col-6 mx-auto",
            ),
        ])

def call_mass_dev_inp():
    '''Call estimated mass deviation drop down menu'''
    return html.Div([
        html.Div([
            '''
            Select the estimated mass deviation of your data (in ppm):
            ''',
            html.A(
                html.Div(
                    "?",
                    id="mass_dev_inp_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
                html.Div(
                    '''
                    Used as precision threshold during different 
                    calculation steps, such as ion adduct 
                    calculation. For more information, 
                    click this info-button to access the docs.
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
            ),
        ])

def call_min_ms2_inpt():
    '''Call minimal nr ms2 fragments input field'''
    return html.Div([
        html.Div([ 
            '''
            Minimal required number of fragments 
            per MS² spectrum:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="min_ms2_inpt_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Quality control parameter.
                If a MS/MS spectrum does not meet the
                requirement, it is dropped, and the
                associated feature is considered MS1 only. 
                MS/MS spectra with a low number of peaks 1)
                have low information content and 2) 
                may lead to false positive similarity 
                assumptions. For more information, 
                click this info-button to access the docs.
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
            ),
        ])

def call_feat_int_filt():
    '''Call feature intensity filter input field'''
    return html.Div([
        html.Div([ 
            '''
            Enter the feature relative intensity filter:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="feat_int_filt_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Value used to filter out low-intensity features 
                ('cut the grass'). Indicates the minimal 
                relative intensity (relative to the feature
                with the highest intensity in the sample)
                a feature must have to be considered for
                further analysis. A value of
                0.05 would exclude all features with a 
                relative intensity below 0.05, i.e. the
                bottom 5% of features; 
                a value of 0 would include all
                features. By default, this value is 0,
                and should be chosen with respect to the 
                underlying data. 
                For more information, 
                click this info-button to access the docs.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="feat_int_filt_tooltip",
            ),
        dbc.Input(
            id='feat_int_filt_inp',
            type='number',
            inputmode='numeric',
            debounce=False,
            value=0, 
            min=0,
            max=0.99,
            step=0.01,
            ),
        ])

def call_bioact_fact_inp():
    '''Call the bioactivity factor input field'''
    return html.Div([
        html.Div([ 
            '''
            Enter the bioactivity factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="bioact_fact_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Factor used in the identification of 
                bioactivity-associated features (if
                bioactivity data was provided). 
                If a feature
                was detected in both bioactive and inactive
                samples, how many times must the feature
                be more intense in the active sample with the lowest
                activity
                than the highest intensity detected in in the 
                inactive samples to be still 
                considered bioactivity-associated. 
                This allows to consider sub-active 
                concentrations.
                For example, a value of 10 would 
                mean that the intensity of a feature must 
                be 10 times higher in a bioactive sample than
                in an inactive sample to be considered 
                bioactivity-associated.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            ),
        ])

def call_column_ret_fact_inp():
    '''Call the column retention factor input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the column retention factor:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="column_ret_fact_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Factor used in the identification of 
                medium-blank/sample-blank associated features (if
                metadata was provided). 
                If a feature
                was detected in both authentic samples and 
                medium/sample blanks, how many times must the feature
                be more intense in sample than in a blank to be 
                still considered sample-associated.
                This calculation takes into account retention of
                compounds by the chromatography column and bleed into
                blank analysis runs. 
                For example, a column retention factor of 10 would mean
                that the average intensity of the features across 
                samples must be 10 times higher than the average 
                intensity across blanks.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            ),
        ])

def call_spec_sim_tol_inp():
    '''Call the spectrum similarity tolerance input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the spectrum similarity tolerance:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_tol_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Tolerance in m/z used in the calculation of spectra 
                similarity scores between MS2 spectra. Two peaks will be 
                considered a match if their difference is less then 
                or equal to the m/z tolerance. Dependent on the 
                precision and mass deviation of the instrument.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            ),
        ])

def call_spec_sim_score_cutoff_inp():
    '''Call the spectrum similarity score cutoff input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the spectrum similarity score cutoff:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_score_cutoff_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Score cutoff used in the evaluation of modified 
                cosine scores between MS2 spectra. Two spectra will be 
                considered related only if their score exceeds the 
                cutoff threshold. Therefore, this parameter controls 
                how strict the similarity between two spectra must be.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            ),
        ])

def call_spec_sim_max_links_inp():
    '''Call the spectrum similarity maximal links input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the maximal number of spectrum similarity links:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_max_links_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Maximal number of links to other nodes, per node. 
                Makes spectral similarity network less convoluted since
                it restricts the number of links between nodes to the 
                highest n ones.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            step=1,
            ),
        ])

def call_spec_sim_min_match_inp():
    '''Call the spectrum similarity minimal matched peaks input field '''
    return html.Div([
        html.Div([ 
            '''
            Enter the minimum number of matched peaks used 
            in spectrum similarity calculation:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="spec_sim_min_match_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                In spectrum similarity matching, the minimum number of 
                peaks that have to be matched between two spectra to be
                considered a match.
                For more information and full reasoning,
                click this info-button to access the docs.
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
            ),
        ])


def call_peaktable_upload():
    '''Call the peaktable upload field'''
    return html.Div([
            html.Span([
                dcc.Upload(
                    html.Button(
                        'Upload peaktable (*_quant_full.csv)',
                        id="upload-peaktable-tooltip",
                        ),
                    id='processing-upload-peaktable'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Reads a MZmine3 style peaktable with the 
                        '_quant_full.csv' suffix
                        (exported in the FULL/ALL mode).
                        For more information on the format, see
                        the documentation.
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
                        'Upload the MS/MS file (*.mgf)',
                        id="upload-mgf-tooltip",
                        ),
                    id='processing-upload-mgf'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Reads a MZmine3 MZmine3 style .mgf-file containing
                        tandem mass (MS/MS) spectra, accompanying
                        the peaktable. Generated through MZmine3 export.
                        For more information on the format, see
                        the documentation.
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
                        'Upload bioactivity table (*.csv)',
                        id="upload-bioactiv-tooltip",
                        ),
                    id='upload-bioactiv'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Bioactivity annotation file in .csv format.
                        FERMO expects on each row a sample name and
                        bioactivity information, which can be in three
                        different formats: 1) the signal word 'active'; 
                        OR 2) a positive integer (whole) number, with
                        the sample with the highest integer considered
                        most active; OR a positive float (dot) number,
                        with the sample with the lowest float considered
                        most active. 
                        For more information on the format, see
                        the documentation.
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
                        'Upload metadata table (*.csv)',
                        id="upload-metadata-tooltip",
                        ),
                    id='upload-metadata'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Metadata annotation file in .csv format.
                        Marks the files that should be considered blanks.
                        FERMO expects on each row a sample name 
                        For more information on the format, see
                        the documentation.
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
                        'Upload spectral library (*.mgf)',
                        id="upload-userlib-tooltip",
                        ),
                    id='upload-userlib'),
                dbc.Tooltip(
                    html.Div(
                        '''
                        Reads a user-provided spectral library in the 
                        .mgf-format.
                        For more information on the format, see
                        the documentation.
                        ''',
                        ),
                    placement='right',
                    className='info_dot_tooltip',
                    target="upload-userlib-tooltip",
                    ),
                ]),
        ])

def call_bioact_type_dd():
    '''Call dropdown menu for bioactivity data specification'''
    return html.Div([
        html.Div([ 
            '''
            Specify the bioactivity table format:
            ''',
            html.A(
                html.Div(
                    "?",
                    id="call_bioact_type_tooltip",
                    className="info_dot"
                    ),
                #DUMMY LINK, SPECIFY CORRECT DOC LINK
                href='https://github.com/mmzdouc/fermo', 
                target='_blank',
                ),
            ]),
        dbc.Tooltip(
            html.Div(
                '''
                Specify the format of the biological activity data.
                Accepts two formats: concentration and percentage.
                For both formats, values must be positive numbers.
                For concentrations, the lowest value will be
                considered the highest activity, and the highest
                value the lowest activity.
                For percentage, the highest value will be considered the 
                highest activity, and the lowest value the lowest activity.
                Samples not listed in the bioactivity table will be 
                considered inactive.
                ''',
                ),
            placement='right',
            className='info_dot_tooltip',
            target="call_bioact_type_tooltip",
            ),
        
        dcc.Dropdown(
            options=[
               {'label': 'Concentration (i.e. lowest value = highest activity)', 'value': 'conc'},
               {'label': 'Percentage (i.e. highest value = highest activity)', 'value': 'perc'},
               ],
            value=None,
            id='bioact_type',
            ),
        ])


processing = html.Div([
    ###first row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('FERMO: Processing mode'),
                ],
            id="processing_row_1_col_1",
            width=12,
            ),
        ],
    id="processing_row_1",
    ),
    ###second row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for a brief par on how the processing mode works'),
                ],
            id="processing_row_2_col_1",
            width=12,
            ),
        ],
    id="processing_row_2",
    ),
    ###third row###
    dbc.Row([
        #first column#
        dbc.Col([
                html.Div('Placeholder for files to upload'),
                html.Hr(),
                call_peaktable_upload(),
                html.Div(
                    id='upload-peaktable-output',
                    style={
                        'color' : 'red',
                        'font-weight' : 'bold',
                        },
                    ),
                html.Hr(),
                #MGF UPLOAD FIELD
                call_mgf_upload(),
                html.Div(
                    id='upload-mgf-output',
                    style={
                        'color' : 'red',
                        'font-weight' : 'bold',
                        },
                    ),
                html.Hr(),
                #BIOACTIVITY UPLOAD FIELD
                call_bioact_type_dd(),
                call_bioactiv_upload(),
                html.Div(
                    id='upload-bioactiv-output',
                    style={
                        'font-weight' : 'bold',
                        },
                    ),
                html.Hr(),
                #METADATA UPLOAD FIELD
                call_metadata_upload(),
                html.Div(
                    id='upload-metadata-output',
                    style={
                        'font-weight' : 'bold',
                        },
                    ),
                html.Hr(),
                #USER LIBRARY UPLOAD FIELD
                call_userlib_upload(),
                html.Div(
                    id='upload-userlib-output',
                    style={
                        'font-weight' : 'bold',
                        },
                    ),
                html.Hr(),
                
                #Helper functions/fields
                html.Div(id='store_bioact_type', hidden=True),
                ],
            id="processing_row_3_col_1",
            width=6,
            ),
        #second column#
        dbc.Col([
                html.Div('Placeholder for parameter settings'),
                html.Hr(),
                call_mass_dev_inp(),
                call_min_ms2_inpt(),
                call_feat_int_filt(),
                call_bioact_fact_inp(),
                call_column_ret_fact_inp(),
                call_spec_sim_tol_inp(),
                call_spec_sim_score_cutoff_inp(),
                call_spec_sim_max_links_inp(),
                call_spec_sim_min_match_inp(),


                ],
            id="processing_row_3_col_2",
            width=6,
            ),
        ],
    id="processing_row_3",
    ),
    ###fourth row###
    dbc.Row([
        #first column#
        dbc.Col([
                call_dashboard_processing_button(),
                
                ###STORAGE###
                #Parameter storage
                html.Div(id='params_cache', hidden=True),
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
                        'text-align' : 'center',
                    })
                ],
            id="processing_row_4_col_1",
            width=12,
            ),
        ],
    id="processing_row_4",
    ),
    ])









