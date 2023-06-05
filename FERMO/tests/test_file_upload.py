from pathlib import Path


def test_upload_folder_exists():
    '''Test if the example file exists'''
    example_file = Path.cwd() / 'FERMO/example_data/FERMO_session.json'
    assert example_file.is_file()
