from dash import html
import io
from pyteomics import mgf
import pandas as pd


###GENERAL

def div_no_file_loaded(filetype):
    '''Return placeholder div if no file loaded
    
    Parameters
    ----------
    filetype : `str`
    '''
    return html.Div(
        f'No {filetype} loaded.'
        )

def div_file_format_error(filename, formatname):
    '''Return div for file format error
    
    Parameters
    ----------
    filename : `str`
    formatname : `str`
    '''
    return html.Div(
        f'''❌ Error: "{filename}" does not seem to be a file
         in the {formatname}-format. Is this the correct file
         for this input field?'''
        )

def div_successful_load_message(filename):
    '''Return div for successful file upload
    
    Parameters
    ----------
    filename : `str`
    
    Notes
    -----
    The specified style overrides the default one in the processing page
    which is red.
    '''
    return html.Div(
        f'✅ "{filename}" successfully loaded.',
        style={
            'color' : 'green', 
            'font-weight' : 'bold',
            }
        )

###PARAMETER VALUES

def test_for_None(value, repl):
    '''Replace value with repl if value is None
    
    Parameters
    ----------
    value : `num or None`
    repl : `num`
    '''
    if value is None:
        return repl
    else:
        return value

def assign_params_to_dict(params_cache):
    '''Assigns parameters to dict
    
    Parameters
    ----------
    params_cache : `dict`
    '''
    return {
        'mass_dev_ppm' : params_cache['mass_dev'],
        'min_nr_ms2' : params_cache['min_ms2'],
        'feature_rel_int_fact' : params_cache['feat_int_filt'],
        'bioact_fact' : params_cache['bioact_fact'],
        'column_ret_fact' : params_cache['column_ret_fact'],
        'spectral_sim_tol' : params_cache['spec_sim_tol'],
        'spec_sim_score_cutoff' : params_cache['spec_sim_score_cutoff'],
        'max_nr_links_ss' : params_cache['spec_sim_max_links'],
        'min_nr_matched_peaks' : params_cache['spec_sim_min_match'],
        'ms2query' : params_cache['ms2query'],
        }

###PEAKTABLE

def div_column_header_error(filename, header):
    '''Return div for column header error
    
    Parameters
    ----------
    filename : `str`
    header : `str`
    '''
    return html.Div(
        f'''
        ❌ Error: "{filename}" is missing column(s) titled "{header}".
        Is this peaktable in the current MZmine3 ALL format? 
        If yes, contact the FERMO developers.
        ''')

def assert_peaktable_format(peaktable, filename):
    """Test peaktable columns for correct headers (i.e. format)
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    
    if peaktable.filter(regex="^id$").columns.empty:
        return div_column_header_error(filename, 'id')
    elif peaktable.filter(regex="^mz$").columns.empty:
        return div_column_header_error(filename, 'mz')
    elif peaktable.filter(regex="^rt$").columns.empty:
        return div_column_header_error(filename, 'rt')
    elif peaktable.filter(regex="^datafile:").columns.empty:
        return div_column_header_error(filename, 'datafile: ...')
    elif peaktable.filter(regex=":intensity_range:max$").columns.empty:
        return div_column_header_error(filename, '... :intensity_range:max')
    elif peaktable.filter(regex=":feature_state$").columns.empty:
        return div_column_header_error(filename, '... :feature_state')
    elif peaktable.filter(regex=":fwhm$").columns.empty:
        return div_column_header_error(filename, '... :fwhm')
    elif peaktable.filter(regex=":rt$").columns.empty:
        return div_column_header_error(filename, '... :rt')
    elif peaktable.filter(regex=":rt_range:min$").columns.empty:
        return div_column_header_error(filename, '... :rt_range:min')
    elif peaktable.filter(regex=":rt_range:max$").columns.empty:
        return div_column_header_error(filename, '... :rt_range:min')
    else:
        return None

###MGF FILE - MS2 DATA

def extract_mgf_for_json_storage(decoded):
    """Convert bytestream from mgf input into dict entries
    
    Parameters
    ----------
    decoded : `bytes`
    
    Returns
    -------
    ms2dict_store : `dict`
    """
    ms2dict_store = dict()
    
    for spectrum in mgf.read(io.StringIO(
            decoded.decode('utf-8')
        ),
        use_index=False
    ):
        fragments = spectrum.get('m/z array')
        intensities = spectrum.get('intensity array')
        feature_ID = int(spectrum.get('params').get('feature_id'))

        ms2dict_store[feature_ID] = [
            fragments.tolist(), 
            intensities.tolist(),
            ]
    
    return ms2dict_store

###QUANTITATIVE BIOLOGICAL DATA

def div_no_quantbio_format(value):
    '''Return div if no quantitative biological data format was specified
    
    Parameters
    ----------
    value : `str`
    '''
    return html.Div(
        f'''❌ Error: Please specify the format of the quantitative
        biological data table. Currently, the value is {value}.
        ''',
        style={
            'color' : 'red', 
            'font-weight' : 'bold',
            }
        )

def assert_bioactivity_format(bioactiv_table, filename):
    """Test bioact table for col headers, empty values and trailing spaces
        
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(bioactiv_table.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif bioactiv_table.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'''❌ Error: "{filename}" is missing a column titled "sample_name".'''
            )
    elif bioactiv_table.filter(regex="^quant_data$").columns.empty:
        return html.Div(
        f'''❌ Error: "{filename}" is missing a column titled "quant_data".'''
            )
    elif bioactiv_table.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'quant_data'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field in column "quant_data" of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'sample_name'].astype(str).str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'quant_data'].dtypes == "object": 
        return html.Div(
        f'''
        ❌ Error: Field containing text values (strings) in column 
        'quant_data' in file {filename} detected.
        This might be also whitespace at the bottom of the column.
        This is not allowed. Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'sample_name'].duplicated().any():
        return html.Div(
        f'''
        ❌ Error: Duplicate values in column 'sample_name'
        in file {filename} detected. This is not allowed.
        Please correct and try again.'''
            )
    else:
        return None


def remove_zero_values_df(df):
    '''Remove rows with zero values from pandas DF
    
    Parameter
    ---------
    df : `pandas.core.frame.DataFrame`
    '''
    return df[df.quant_data != 0]


def parse_bioactiv_conc(bioactiv_table, value):
    """Parses quantitative biological data table and converts values
    
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    value : `str`
    
    Returns
    --------
    converted_df : `pandas.core.frame.DataFrame`
    
    Notes
    ------
    For reference to 'normalization#, refer to:
    Normalization calculation:
    #Stephan Kolassa 
    #(https://stats.stackexchange.com/users/1352/stephan-kolassa),
    #"scale a number between a range", 
    #URL (version: 2018-04-19): https://stats.stackexchange.com/q/281164
    """
    #scale to 0.1-1.0, lowest becomes highest (0 reserved for inactive)
    if value == 'conc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['quant_data'] == bioactiv_table['quant_data'][0]).all():
            normalized = bioactiv_table.loc[:,'quant_data'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'quant_data'].apply(
                lambda x: (1 / x))
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df

    #scale to 0.1-1 (for reference, see above)
    elif value == 'perc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['quant_data'] == bioactiv_table['quant_data'][0]).all():
            normalized = bioactiv_table.loc[:,'quant_data'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'quant_data'].apply(
                lambda x: x)
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df

###METADATA

def assert_metadata_format(metadata, filename):
    """Test metadata table for col headers, false values and trailing spaces
    
    Parameters
    ----------
    metadata : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(metadata.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif metadata.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'''❌ Error: "{filename}" is missing a column titled "sample_name".'''
            )
    elif metadata.filter(regex="^attribute$").columns.empty:
        return html.Div(
        f'''❌ Error: "{filename}" is missing a column titled "attribute".'''
            )
    elif metadata.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in column 'sample_name' of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^GENERAL$').any():
        return html.Div(
        f'''
        ❌ Error: Signal word "GENERAL" used in file {filename}.
        This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'attribute' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].duplicated().any():
        return html.Div(
        f'''
        ❌ Error: Duplicate values in column 'sample_name'
        in file {filename} detected. This is forbidden.'''
            )
    else:
        return None

###SPECTRAL LIBRARY

def prepare_spec_lib_for_json_storage(decoded):
    """Convert bytestream from mgf input into dict entries
    
    Parameters
    ----------
    decoded : `bytes`
    
    Returns
    -------
    reflib_dict : `dict`
    """
    reflib_dict = dict()
    counter = 1
    
    for spectrum in mgf.read(io.StringIO(
        decoded.decode('utf-8')
        ),
        use_index=False,
    ):
        mz = spectrum.get('m/z array')
        intensities = spectrum.get('intensity array')
        metadata = spectrum.get('params')
        reflib_dict[counter] = [
            mz.tolist(), 
            intensities.tolist(), 
            metadata
            ]
        counter = counter + 1
    
    return reflib_dict

###SESSION FILE LOADING

def div_session_version_warning(filename, df, __version__):
    '''Return div for file format error
    
    Parameters
    ----------
    filename : `str`
    df : `pandas.core.frame.DataFrame`
    __version__ : `str`
    '''
    return html.Div(
        f'''❗ Warning: The loaded session file "{filename}"
        has been created using "{df.at[2,'Description']}",
        while the currently running version is "{__version__}". 
        This might lead to unforseen behaviour of the application.
        ''')

def empty_loading_table():
    '''Generate empty table for loading page'''
    content = [
                ['Date of creation', None],
                ['Time of creation', None],
                ['FERMO version', None],
                ['-----', '-----'],
                ['Filename: peaktable', None],
                ['Filename: MS² data', None],
                ['Filename: group metadata', None],
                ['Filename: quantitative biological data', None],
                ['Filename: user-library', None],
                ['-----', '-----'],
                ['Mass deviation', None],
                ['Min fragments per MS² spectrum', None],
                ['Relative intensity filter', None],
                ['QuantData factor', None],
                ['Blank factor', None],
                ['Fragment similarity tolerance', None],
                ['Spectrum similarity score cutoff', None],
                ['Max spectral links', None],
                ['Min matched peaks', None],
            ]
    return pd.DataFrame(content, columns=['Attribute', 'Description'])

def session_loading_table(params, files, metadata, version):
    '''Generate table to return upon session loading on loading page'''
    content = [
                ['Date of creation', metadata['date']],
                ['Time of creation', metadata['time']],
                ['FERMO version', version],
                ['-----', '-----'],
                ['Filename: peaktable', files['peaktable_name']],
                ['Filename: MS² data', files['mgf_name']],
                ['Filename: group metadata', files['metadata_name']],
                ['Filename: quantitative biological data', files['bioactivity_name']],
                ['Filename: user-library', files['user_library_name']],
                ['-----', '-----'],
                ['Mass deviation', params['mass_dev_ppm']],
                ['Min fragments per MS² spectrum', params['min_nr_ms2']],
                ['Relative intensity filter', params['feature_rel_int_fact']],
                ['QuantData factor', params['bioact_fact']],
                ['Blank factor', params['column_ret_fact']],
                ['Fragment similarity tolerance', params['spectral_sim_tol']],
                ['Spectrum similarity score cutoff', params['spec_sim_score_cutoff']],
                ['Max spectral links', params['max_nr_links_ss']],
                ['Min matched peaks', params['min_nr_matched_peaks']],
            ]
    return pd.DataFrame(content, columns=['Attribute', 'Description'])
