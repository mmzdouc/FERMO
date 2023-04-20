from pathlib import Path
from flask import flash
import json
from json.decoder import JSONDecodeError


def load_example(path: str) -> dict:
    '''Load example session file

    Parameters
    ----------
    path: `str`
        Path to the example session file

    Returns
    -------
    return_value: `dict`
        If loading was successfull return the loaded data, otherwise return
        empty dictionary
    '''
    try:
        with open(Path.cwd() / path) as f:
            data_dict = json.load(f)
    except (FileNotFoundError, JSONDecodeError) as e:
        print(e)
        return_value = {}
        flash(f'Example data could not be loaded: {e}')
    else:
        return_value = data_dict
    finally:
        return return_value


def access_loaded_data(loaded_data: dict):
    '''Access elements of loaded data

    Parameters
    ----------
    loaded_data: `dict`

    Returns
    -------
    sample_stats: `dict`
    samples_json: `dict`
        dict in json-format -> must be accessed via json.loads() first to
        convert to proper dictionary
    samples_dict: `dict`
    feature_dicts: `dict`
    '''
    sample_stats = loaded_data['sample_stats']
    samples_json = loaded_data['samples_JSON']
    samples_dict = sample_stats['samples_dict']
    feature_dicts = loaded_data['feature_dicts']

    return sample_stats, samples_json, samples_dict, feature_dicts
