from werkzeug.utils import secure_filename
import os
import json

# for type hinting
from typing import Tuple
from werkzeug.datastructures import FileStorage


def check_file_format(
    filename: str,
    file_format: str,
    allowed_extensions: list,
) -> (str):
    ''' Check filename for validity

    Parameters
    ----------
    filename: `str`
    file_format: `str`
        File format of one specific input with the leading dot
    allowed_extension: `list`
        List of strings as specified in config file

    Return
    ------
    feedback: `str`
        String with feedback for the user to be flashed
    '''
    if '.' not in file_format:
        raise ValueError(
            'file_format should be specified with the leading dot'
        )
    elif file_format not in allowed_extensions:
        raise ValueError(
            '''file_format must be an allowed_extension as specified in
            the config'''
        )
    elif filename == '':
        feedback = 'No file was loaded. Please upload a session-file.'
    elif not filename.endswith(file_format):
        feedback = f"File must be a {file_format}-file!"
    else:
        feedback = ''
    return feedback


def save_file(
        file: FileStorage,
        file_format: str,
        allowed_extensions: list,
        upload_folder: str,
) -> Tuple[str, str]:
    '''Save the file if it is valid

    Parameters
    ----------
    file: `werkzeug.datastructures.FileStorage`
        An element of request.files
    file_format: `str`
        File format of one specific input with the leading dot
    allowed_extensions: `list`
        List of str, as specified in config file
    upload_folder: `str`
        Path to location where files should be stored

    Return
    ------
    `str`
        Feedback for the user to be flashed or the secure filename of the saved
        file
    `bool`
        True if file-saving was successfull, False otherwise

    Notes
    -----
    Checks if a file was provided and if it has the right format (judging
    by the filename). If so, the file is saved in the 'upload_folder'
    '''
    filename = secure_filename(file.filename)
    feedback = check_file_format(
            filename,
            file_format,
            allowed_extensions,
        )
    if feedback:
        return feedback, False
    else:
        try:
            file.save(os.path.join(upload_folder, filename))
            return filename, True
        except FileNotFoundError as e:
            print(e)
            feedback = '''File or folder did not exist, so the uploaded file
            could not be saved'''
            return feedback, False


def check_version(content_dict: dict, filename: str, version: str) -> str:
    '''Compare version of uploaded file with current FERMO-version

    Parameters
    ----------
    content_dict: `dict`
        From opened json file
    filename: `str`
    version: `str`
        Version of the running tool

    Return
    ------
    `str`
        Error/warning message if versions are(may) not (be) compatible,
        empty string otherwise
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
        return ''


def empty_loading_table() -> list:
    '''Generate placeholder table for loading page

    Returns
    -------
    `list`
        List of lists: placeholder for table before file upload
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
    params: dict,
    files: dict,
    metadata: dict,
    version: dict,
    logging: dict,
) -> list:
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
    `list`
        List of lists with session file info
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


def parse_sessionfile(
    filename: str,
    version: str,
    upload_folder: str,
) -> Tuple[list, str]:
    '''Check version compatibility and create session file

    Parameters
    ----------
    filename: `str`
    version: `str`
        Current version of FERMO as read from __version__.py file
    upload_folder: `str`
        location were uploaded files are stored

    Return
    ------
    `list`
        Containing the parsed file info
    `str`
        Message for (possible) incompatibility or FileNotFoundError
    '''
    try:
        with open(
            os.path.join(upload_folder, filename)
        ) as f:
            content_dict = json.load(f)
            table_list = create_session_table(
                content_dict['params_dict'],
                content_dict['input_filenames'],
                content_dict['session_metadata'],
                content_dict['FERMO_version'],
                content_dict['logging_dict'],
            )
            message = check_version(content_dict, filename, version)
            return table_list, message
    except FileNotFoundError as file_error:
        print(file_error)
        return empty_loading_table(), 'FileNotFoundError'
    except KeyError as key_error:
        print(key_error)
        os.remove(os.path.join(upload_folder, filename))
        return (
            empty_loading_table(),
            'Make sure the file is from a previous session!'
        )
