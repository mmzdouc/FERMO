import copy
from pathlib import Path
import re
from flask import flash
import json
from json.decoder import JSONDecodeError

import pandas as pd


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
    samples_json_dict: `dict`
        Dictionary with samples as first keys and all other information as
        (nested) values
    samples_dict: `dict`
    feature_dicts: `dict`
    '''
    sample_stats = loaded_data['sample_stats']
    samples_dict = sample_stats['samples_dict']

    samples_json_dict = {}
    samples_json = loaded_data['samples_JSON']
    for sample in samples_dict:
        samples_json_dict[sample] = pd.read_json(
            samples_json[sample], orient='split'
        )

    feature_dicts = loaded_data['feature_dicts']

    return sample_stats, samples_json_dict, samples_dict, feature_dicts


def generate_subsets(
    samples_json_dict: dict,
    sample: str,
    thresholds: dict,
    feature_dicts: dict,
) -> dict:
    """Make subsets of features in sample based on thresholds

    Parameters
    ----------
    samples_json_dict: `dict`
        dictionary with loaded 'json' information e.g. output from 
        access_loaded_data()
    sample: `str`
    thresholds: `dict`
    feature_dicts: `dict`

    Returns
    --------
    `dict`

    Notes
    ------
    Additional filters can be added with relative ease:
    Add the filter to the FERMO dashboard
    Connect filter to the callback id calculate_feature_score
    Simply add a conditional that adds feature ID to "all_select_no_blank"
    set. the later operations take care of the right group for plotting

    Example code: extract a row as series using squeeze()
    samples[selected_sample].loc[samples[selected_sample]
    ['feature_ID'] == ID].squeeze(),
    """
    all_feature_set = set(samples_json_dict[sample]['feature_ID'])

    features_blanks_set = set()
    for feature_ID in all_feature_set:
        if 'BLANK' in feature_dicts[str(feature_ID)]['set_groups']:
            features_blanks_set.add(feature_ID)

    ms1_only_df = samples_json_dict[sample].loc[
        samples_json_dict[sample]['ms1_only'] == True
        ]
    ms1_only_set = set(ms1_only_df['feature_ID'])

    blank_ms1_set = ms1_only_set
    all_nonblank_set = all_feature_set.difference(blank_ms1_set)
    if thresholds['blank_designation_toggle'] == 'DESIGNATE':
        blank_ms1_set = features_blanks_set.union(ms1_only_set)
        all_nonblank_set = all_feature_set.difference(blank_ms1_set)

    # filter for numeric thresholds
    filt_df = samples_json_dict[sample].loc[
        ((samples_json_dict[sample]['rel_intensity_score']
          >= thresholds['rel_intensity_threshold'][0])
         & (
            samples_json_dict[sample]['rel_intensity_score']
            <= thresholds['rel_intensity_threshold'][1]
        )) &
        ((samples_json_dict[sample]['novelty_score']
            >= thresholds['novelty_threshold'][0])
         & (samples_json_dict[sample]['novelty_score']
            <= thresholds['novelty_threshold'][1])
         ) &
        ((samples_json_dict[sample]['convolutedness_score']
            >= thresholds['peak_overlap_threshold'][0])
         & (samples_json_dict[sample]['convolutedness_score']
            <= thresholds['peak_overlap_threshold'][1])
         )
    ]
    filtered_thrsh_set = set(filt_df['feature_ID'])

    if thresholds['quant_biological_value'] != 'OFF':
        temp_set = set()
        if thresholds['quant_biological_value'] == 'SPECIFICITY':
            for feature in filtered_thrsh_set:
                if feature_dicts[str(feature)]['bioactivity_associated']:
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)
        elif thresholds['quant_biological_value'] == 'SPEC.+TREND':
            for feature in filtered_thrsh_set:
                if (
                    feature_dicts[str(feature)]['bioactivity_associated']
                    &
                    feature_dicts[str(feature)]['bioactivity_trend']
                ):
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_adduct_isotopes'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            if filter_str_regex(
                thresholds['filter_adduct_isotopes'],
                ','.join([i for i in feature_dicts[str(feature)][
                    'ann_adduct_isotop'
                ]]),
            ):
                temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_annotation'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            search_list = ['',]
            if feature_dicts[str(feature)]['ms2query']:
                search_list.append(
                    feature_dicts[str(feature)][
                        'ms2query_results'][0]['analog_compound_name']
                    )
            if feature_dicts[str(feature)]['cosine_annotation']:
                search_list.append(
                    feature_dicts[str(feature)][
                        'cosine_annotation_list'][0]['name']
                )
            if filter_str_regex(
                thresholds['filter_annotation'],
                ','.join([i for i in search_list])
            ):
                temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_feature_id'] != '':
        if thresholds['filter_feature_id'] in filtered_thrsh_set:
            filtered_thrsh_set = set([thresholds['filter_feature_id']])
        else:
            filtered_thrsh_set = set()

    if (
        thresholds['filter_precursor_min'] != '' or
        thresholds['filter_precursor_max'] != ''
    ):
        mz_min = None
        mz_max = None
        if thresholds['filter_precursor_min'] != '':
            mz_min = float(thresholds['filter_precursor_min'])
        if thresholds['filter_precursor_max'] != '':
            mz_max = float(thresholds['filter_precursor_max'])

        if (mz_min is not None) and (mz_max is not None):
            temp_set = set()
            if mz_min > mz_max:
                temp_min = copy.deepcopy(mz_max)
                temp_max = copy.deepcopy(mz_min)
                mz_min = temp_min
                mz_max = temp_max

            for feature in filtered_thrsh_set:
                if ((
                    mz_min <= feature_dicts[str(feature)]['precursor_mz']
                           <= mz_max
                )):
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

        elif (mz_min is not None) and (mz_max is None):
            temp_set = set()
            for feature in filtered_thrsh_set:
                if mz_min <= feature_dicts[str(feature)]['precursor_mz']:
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

        elif (mz_min is None) and (mz_max is not None):
            temp_set = set()
            for feature in filtered_thrsh_set:
                if feature_dicts[str(feature)]['precursor_mz'] <= mz_max:
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_spectral_sim_netw'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            if feature_dicts[str(feature)]['similarity_clique']:
                if (
                    thresholds['filter_spectral_sim_netw'] ==
                    feature_dicts[str(feature)]['similarity_clique_number']
                ):
                    temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_group'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            if filter_str_regex(
                thresholds['filter_group'],
                ','.join([i for i in feature_dicts[str(feature)]
                          ['set_groups']]),
            ):
                temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_group_cliques'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            try:
                if filter_str_regex(
                    thresholds['filter_group_cliques'],
                    ','.join([i for i in feature_dicts[str(feature)][
                        'set_groups_clique']]),
                ):
                    temp_set.add(feature)
            except:
                pass
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if thresholds['filter_samplename'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            try:
                if filter_str_regex(
                    thresholds['filter_samplename'],
                    ','.join([i for i in feature_dicts[str(feature)][
                        'presence_samples']]),
                ):
                    temp_set.add(feature)
            except:
                pass
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    if (
        thresholds['filter_samplenumber_min'] != '' or
        thresholds['filter_samplenumber_max'] != ''
    ):
        snum_min = None
        snum_max = None
        if thresholds['filter_samplenumber_min'] != '':
            snum_min = float(thresholds['filter_samplenumber_min'])
        if thresholds['filter_samplenumber_max'] != '':
            snum_max = float(thresholds['filter_samplenumber_max'])

        if (snum_min is not None) and (snum_max is not None):
            temp_set = set()
            if snum_min > snum_max:
                temp_min = copy.deepcopy(snum_max)
                temp_max = copy.deepcopy(snum_min)
                snum_min = temp_min
                snum_max = temp_max

            for feature in filtered_thrsh_set:
                if ((
                    snum_min
                    <= len(feature_dicts[str(feature)]['presence_samples'])
                    <= snum_max
                )):
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

        elif (snum_min is not None) and (snum_max is None):
            temp_set = set()
            for feature in filtered_thrsh_set:

                if snum_min <= len(
                    feature_dicts[str(feature)]['presence_samples']
                ):
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

        elif (snum_min is None) and (snum_max is not None):
            temp_set = set()
            for feature in filtered_thrsh_set:
                if (
                    len(feature_dicts[str(feature)]['presence_samples'])
                    <= snum_max
                ):
                    temp_set.add(feature)
            filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    # Fold-changes: Include
    if (
        (thresholds['filter_fold_greater_int'] != '')
        and
        (thresholds['filter_fold_greater_regex'] == '')
    ):
        temp_set = set()
        for feature in filtered_thrsh_set:
            if feature_dicts[str(feature)]['dict_fold_diff']:
                for i in feature_dicts[str(feature)]['dict_fold_diff']:
                    if (
                        feature_dicts[str(feature)]['dict_fold_diff'][i]
                        >=
                        float(thresholds['filter_fold_greater_int'])
                    ):
                        temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)
    elif (
        (thresholds['filter_fold_greater_int'] != '')
        and
        (thresholds['filter_fold_greater_regex'] != '')
    ):
        temp_set = set()
        for feature in filtered_thrsh_set:
            if feature_dicts[str(feature)]['dict_fold_diff']:
                for i in feature_dicts[str(feature)]['dict_fold_diff']:
                    if ((
                        feature_dicts[str(feature)]['dict_fold_diff'][i]
                        >= float(thresholds['filter_fold_greater_int'])
                        )
                        and (filter_str_regex(
                            thresholds['filter_fold_greater_regex'], i,
                        )
                    )):
                        temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)

    # Fold-changes: exclude
    if (
        (thresholds['filter_fold_greater_exclude_int'] != '')
        and
        (thresholds['filter_fold_greater_exclude_regex'] == '')
    ):
        temp_set = set()
        for feature in filtered_thrsh_set:
            if feature_dicts[str(feature)]['dict_fold_diff']:
                for i in feature_dicts[str(feature)]['dict_fold_diff']:
                    if (
                        feature_dicts[str(feature)]['dict_fold_diff'][i]
                        >=
                        float(thresholds['filter_fold_greater_exclude_int'])
                    ):
                        temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.difference(temp_set)
    elif (
        (thresholds['filter_fold_greater_exclude_int'] != '')
        and
        (thresholds['filter_fold_greater_exclude_regex'] != '')
    ):
        temp_set = set()
        for feature in filtered_thrsh_set:
            if feature_dicts[str(feature)]['dict_fold_diff']:
                for i in feature_dicts[str(feature)]['dict_fold_diff']:
                    if ((
                        feature_dicts[str(feature)]['dict_fold_diff'][i]
                            >= float(thresholds[
                                'filter_fold_greater_exclude_int'
                                ])
                        ) and (
                            filter_str_regex(thresholds[
                            'filter_fold_greater_exclude_regex'
                            ], i,)
                    )):
                        temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.difference(temp_set)

    # subtract ms1 and blanks from features over threshold
    all_select_no_blank = filtered_thrsh_set.difference(blank_ms1_set)

    # subset of selected sample specific features
    select_sample_spec = set()
    for ID in all_select_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            select_sample_spec.add(ID)

    # subset of selected group specific features
    select_group_spec = set()
    for ID in all_select_no_blank.difference(select_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            select_group_spec.add(ID)

    # subtract sample spec and group spec features from total
    select_remainder = all_select_no_blank.difference(select_sample_spec)
    select_remainder = select_remainder.difference(select_group_spec)

    # non-selected features (subtracted blanks+ms1)
    all_nonsel_no_blank = all_nonblank_set.difference(all_select_no_blank)

    # subset of nonselected sample specific features
    nonselect_sample_spec = set()
    for ID in all_nonsel_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            nonselect_sample_spec.add(ID)

    # subset of nonselected group specific features
    nonselect_group_spec = set()
    for ID in all_nonsel_no_blank.difference(nonselect_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            nonselect_group_spec.add(ID)

    # subtract sample spec and group spec features from total
    nonselect_remainder = all_nonsel_no_blank.difference(nonselect_sample_spec)
    nonselect_remainder = nonselect_remainder.difference(nonselect_group_spec)

    return {
        # GENERAL
        'all_features': list(all_feature_set),
        'blank_ms1': list(blank_ms1_set),
        'all_nonblank': list(all_nonblank_set),
        # SELECTED
        'all_select_no_blank': list(all_select_no_blank),
        'select_sample_spec': list(select_sample_spec),
        'select_group_spec': list(select_group_spec),
        'select_remainder': list(select_remainder),
        # NONSELECTED
        'all_nonsel_no_blank': list(all_nonsel_no_blank),
        'nonselect_sample_spec': list(nonselect_sample_spec),
        'nonselect_group_spec': list(nonselect_group_spec),
        'nonselect_remainder': list(nonselect_remainder),
    }


def default_filters() -> dict:
    ''' Generate a dictionary with default filter (threshhold) values

    Returns
    -------
    `dict`
    '''
    return {
        'rel_intensity_threshold': [0, 1],
        'filter_adduct_isotopes': '',
        'quant_biological_value': 'OFF',
        'novelty_threshold': [0, 1],
        'filter_annotation': '',
        'filter_feature_id': '',
        'filter_precursor_min': 0,
        'filter_precursor_max': '',
        'filter_spectral_sim_netw': '',
        'filter_group': '',
        'filter_group_cliques': '',
        'peak_overlap_threshold': [0, 1],
        'filter_samplename': '',
        'filter_samplenumber_min': '',
        'filter_samplenumber_max': '',
        'blank_designation_toggle': 'DESIGNATE',
        'filter_fold_greater_int': '',
        'filter_fold_greater_regex': '',
        'filter_fold_greater_exclude_int': '',
        'filter_fold_greater_exclude_regex': '',
    }


def filter_str_regex(query: str, annot_str: str,) -> bool:
    '''Check if query matches annot_str

    Parameters
    ----------
    query: `str`
    annot_str: `str`

    Returns
    -------
    `bool`
    '''
    try:
        match = bool(re.search(query, annot_str, re.IGNORECASE))
    except:
        return False
    else:
        if match:
            return True
        else:
            return False
