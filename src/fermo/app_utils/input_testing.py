from flask import (
    flash,
    current_app,  # allows to access the config elements
    request,
)
from werkzeug.utils import secure_filename
import os
import json


def allowed_file(filename):
    ''' Returns boolean for valid filenames and allowed extensions

    Parameters
    ----------
    filename : 'str'

    Notes
    -----
    Check for dot in filename and allowed extensions as specified in the
    config file
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
        current_app.config.get('ALLOWED_EXTENSION')


def save_file(inputID, file_format):
    '''Check file for validity and save it

    Parameters
    ----------
    inputID: 'str'
    file_format: 'str'

    Return
    ------
    'str': filename if user input was valid,
    none otherwise

    Notes
    -----
    Checks if the file was succesfully transmitted via request, if a filename
    provided, and if it has the right format. If so, the file is saved in the
    location specified in config.toml under 'UPLOAD_FOLDER'.
    inputID must be taken from the corresponding html file.
    '''
    if inputID not in request.files:
        flash('Something went wrong, please try again')
        return None
    file = request.files[inputID]
    if file.filename == '':
        flash('No file was loaded. Please upload a session-file.')
        return None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename.endswith(file_format):
            try:
                file.save(os.path.join(current_app.config.get(
                    'UPLOAD_FOLDER'), filename))
            except FileNotFoundError:
                print("File or folder didn't exist, \
                        so the uploaded file couldn't be saved")
            return filename
        else:
            flash(f"File must be a {file_format}-file!")
            return None
    else:
        print('something went wrong with the file upload of element:', inputID)
        return None


def check_version(content_dict, filename, version):
    '''Compare version of uploaded file with current FERMO-version

    Parameters
    ----------
    content_dict: 'dict' from opened json file

    Return
    ------
    'str': Error/warning message if versions are(may) not (be) compatible,
    none otherwise
    '''
    uploaded_version = content_dict['FERMO_version']
    uploaded_version_split = uploaded_version.split('.')
    major, minor, fix = (
        uploaded_version_split[0],
        uploaded_version_split[1],
        uploaded_version_split[2],
        )
    if major != version.split('.')[0] or \
       minor != version.split('.')[1]:
        return f'''❌ Error: The loaded session file "{filename}"
        has been created using FERMO version {uploaded_version}.
        This is incompatible with the currently running version
        of FERMO ({version}). Please re-process your data or
        use another version of FERMO.'''
    elif fix != version.split('.')[2]:
        return f'''❗ Warning: The loaded session file "{filename}"
        has been created using FERMO version {uploaded_version}. The
        currently running version of FERMO is {version}.
        While these versions should be compatible, there might be
        some unforseen behavior of the application.'''
    else:
        return None


def empty_loading_table():
    '''Generate placeholder table for loading page

    Returns
    -------
    list of lists: placeholder pre-file-upload
    '''
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
        ['Minimum number of fragments per MS² spectrum', None],
        ['QuantData factor', None],
        ['Blank factor', None],
        ['Relative intensity filter range', None],
        ['Spectral similarity networking algorithm', None],
        ['Fragment similarity tolerance', None],
        ['Spectrum similarity score cutoff', None],
        ['Maximum number of links to each feature in spectral network', None],
        ['Minimum number of matched peaks in spectral similarity matching',
         None],
        ['MS2Query used', None],
        ['MS2Query blank annotation', None],
        ['MS2Query relative intensity range', None],
        ['-----', '-----'],
        ['Process log step', 'Description'],
        ]
    return content


def create_session_table(
    params,
    files,
    metadata,
    version,
    logging
):
    '''Parse session file and generate overview table

    Parameters
    ----------
    params : `dict`
    files : `dict`
    metadata : `dict`
    version : `dict`
    logging : `dict`

    Returns
    -------
    list of lists: session file info
    '''
    content = [
        ['Date of creation', metadata['date']],
        ['Time of creation', metadata['time']],
        ['FERMO version', version],
        ['-----', '-----'],
        ['Filename: peaktable', files['peaktable_name']],
        ['Filename: MS² data', files['mgf_name']],
        ['Filename: group metadata', files['metadata_name']],
        ['Filename: quantitative biological data',
            files['bioactivity_name']],
        ['Filename: user-library', files['user_library_name']],
        ['-----', '-----'],
        ['Mass deviation', params['mass_dev_ppm']],
        ['Minimum number of fragments per MS² spectrum',
            params['min_nr_ms2']],
        ['QuantData factor', params['bioact_fact']],
        ['Blank factor', params['column_ret_fact']],
        ['Relative intensity filter range',
            '-'.join([str(i) for i in params[
                'relative_intensity_filter_range']])],
        ['Spectral similarity networking algorithm',
            params['spec_sim_net_alg']],
        ['Fragment similarity tolerance', params['spectral_sim_tol']],
        ['Spectrum similarity score cutoff',
            params['spec_sim_score_cutoff']],
        ['Maximum number of links to each feature in spectral network',
            params['max_nr_links_ss']],
        ['Minimum number of matched peaks in spectral similarity matching',
            params['min_nr_matched_peaks']],
        ['MS2Query used', params['ms2query']],
        ['MS2Query blank annotation', params['ms2query_blank_annotation']],
        ['MS2Query relative intensity range',
            '-'.join([str(i) for i in params['ms2query_filter_range']])],
        ['-----', '-----'],
        ['Process log step', 'Description'],
        ]
    for entry in logging:
        content.append([entry, logging[entry]])
    return content


def parse_sessionfile(filename, version):
    '''Check version compatibility and create session file

    Parameters
    ----------
    filename: 'str'
    version: 'str'; current version of FERMO as read from __version__.py file

    Return
    ------
    'dict': containing the parsed file info
    'str': message for (possible) incompatibility or Errors
    '''
    try:
        with open(os.path.join(current_app.config.get('UPLOAD_FOLDER'),
                               filename)) as f:
            content_dict = json.load(f)
            table_dict = create_session_table(content_dict['params_dict'],
                                              content_dict['input_filenames'],
                                              content_dict['session_metadata'],
                                              content_dict['FERMO_version'],
                                              content_dict['logging_dict'])
            message = check_version(content_dict, filename, version)
            return table_dict, message
    except FileNotFoundError as e:
        print(e)
        return empty_loading_table(), 'FileNotFoundError'
