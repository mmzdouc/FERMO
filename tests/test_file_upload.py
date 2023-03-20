import io
import json
import os
import pytest
from werkzeug.datastructures import FileStorage
from fermo.app_utils.input_testing import (
    check_file_format,
    save_file,
    # check_version,
    # create_session_table,
    parse_sessionfile,
)

# FIXTURES #


@pytest.fixture
def allowed_extensions():
    return ['.mgf', '.json', '.csv']


@pytest.fixture
def upload_folder():
    return 'src/fermo/uploads/'


@pytest.fixture
def session_file():
    content = {
        "feature_dicts": {1: {}, 2: {}},
        "samples_JSON": {"mod.mzXML": {}, "": {}},
        "samples_stats": {"attribute": {}, "attribute2": []},
        "params_dict": {"param": ''},
        "input_filenames": {},
        "session_metadata": {'date': '', 'time': ''},
        "FERMO_version": "0.9.0",
        "logging_dict": {}
    }
    input_json = json.dumps(content, indent=4).encode('utf-8')
    mock_session_file = FileStorage(
         stream=io.BytesIO(input_json),
         filename='sessionFile.json',
    )
    return mock_session_file


# TESTS #


@pytest.mark.parametrize('filename, file_format', [
    ('metadata.csv', '.csv'),
    ('sessionfile.json', '.json'),
    ('MSMS.mgf', '.mgf'),
])
def test_check_file_format_valid(filename, file_format, allowed_extensions):
    '''Test valid input for check_file_format()'''
    assert not check_file_format(filename, file_format, allowed_extensions)


@pytest.mark.parametrize('filename, file_format', [
    ('metadatacsv', '.csv'),
    ('sessionfile_json', '.json'),
    ('MSMS.txt', '.mgf'),
    ('metadata.csv.txt', '.csv'),
])
def test_check_file_format_invalid(filename, file_format, allowed_extensions):
    '''Test invalid input for check_file_format()'''
    # with pytest.raises, ('metadata.txt', '.txt')
    assert check_file_format(filename, file_format, allowed_extensions)


@pytest.mark.parametrize(
    'filename, file_format',
    [('metadata.txt', '.txt'), ('sessionfile.json', 'json')]
)
def test_check_file_format_raise(filename, file_format, allowed_extensions):
    '''Test input that should raise an error in check_file_format()'''
    with pytest.raises(ValueError):
        check_file_format(filename, file_format, allowed_extensions)


def test_save_file_successfully(
    allowed_extensions,
    session_file,
    upload_folder,
):
    filename, success = save_file(
        session_file,
        '.json',
        allowed_extensions,
        upload_folder,
        )
    assert success
    assert os.path.isfile(os.path.join(upload_folder, filename))
    os.remove(os.path.join(upload_folder, filename))


def test_save_file_nofilename(allowed_extensions, upload_folder):
    '''Test outcome when the filename is empty (user did not upload a file)'''
    message, filename = save_file(
        FileStorage(filename=''),
        '.json',
        allowed_extensions,
        upload_folder,
    )
    expected_message = 'No file was loaded. Please upload a session-file.'
    assert message == expected_message and not filename


def test_parse_sessionfile(session_file, upload_folder):
    '''Test session-file parsing with incomplete sessionfile

    Notes
    -----
    Save a file that mimicks a session file but doesn't have all the necessary
    keys for test purposes in the upload folder, parse it and make sure
    the correct message is returned before removing the file at the end
    '''
    filename = 'testfile'
    should_version = '0.9.0'
    session_file.save(os.path.join(upload_folder, filename))
    table_list, message = parse_sessionfile(
        filename,
        should_version,
        upload_folder,
    )
    expected_message = 'Make sure the file is from a previous session!'
    assert message == expected_message and isinstance(table_list, list)
    os.remove(os.path.join(upload_folder, filename))
