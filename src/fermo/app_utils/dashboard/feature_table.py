import pandas as pd


def update_feature_table(
    selected_sample: str,
    feature_dicts: dict,
    samples_json_dict: dict,
    sample_stats,
    feature_id: int = 1,
    feature_index: int = 0,
) -> dict:
    '''Return feature table for selected feature

    Parameters
    ----------
    selected_sample: `str`
    feature_ID: `int`
    feature_index: `int`
    loaded_data: `dict`

    Returns
    -------
    `dict`
    '''
    if isinstance(feature_index, int):
        return collect_feature_info(
            selected_sample,
            feature_id,
            feature_index,
            feature_dicts,
            samples_json_dict,
            sample_stats,
        )
    else:
        return empty_feature_info_df()


def collect_feature_info(
    smpl: str,
    ID: int,
    index: int,
    feature_dicts: dict,
    samples: dict,
    sample_stats: dict,
) -> list:
    '''Collect info of selected feature for display in feature table

    Parameters
    ----------
    smpl: `str`
    ID: `int`
    index: `int`
    feature_dicts: `dict`
    samples: `dict`
    sample_stats: `dict`

    Returns
    -------
    `list`
        List of lists to build the feature table
    '''
    # change to str for feature dict querying
    ID = str(ID)

    # Intensity per sample
    int_sample = ''.join(
        [str(samples[smpl].at[index, 'intensity']), ' (', smpl, ')',]
    )

    # best cosine match
    cosine_annotation = None
    if feature_dicts[ID]['cosine_annotation']:
        cosine_annotation = ''.join([
            'Name: <b>',
            feature_dicts[ID]['cosine_annotation_list'][0]['name'],
            '</b>;',
            '<br>',
            'Score: ',
            str(feature_dicts[ID]['cosine_annotation_list'][0]['score']),
            ';',
            '<br>',
            'Nr of matched fragments: ',
            str(feature_dicts[ID]['cosine_annotation_list'][0]['nr_matches']),
        ])

    # Best ms2query match
    ann_ms2query = None
    mass_diff_ms2query = None
    class_ms2query = None
    superclass_ms2query = None
    if feature_dicts[ID]['ms2query']:
        ann_ms2query = ''.join([
            'Name: ',
            feature_dicts[ID]['ms2query_results'][0]['Link'],
            ';',
            '<br>',
            'Score: ',
            str(round(feature_dicts[ID]
                                   ['ms2query_results']
                                   [0]
                                   ['ms2query_model_prediction'],
                      3)),
        ])
        mass_diff_ms2query = ''.join([
            'Δ ',
            str(round(feature_dicts[ID]
                                   ['ms2query_results']
                                   [0]
                                   ['precursor_mz_difference'],
                      3)),
            ' <i>m/z</i> (',
            str(round(feature_dicts[ID]['ms2query_results'][0]
                ['precursor_mz_analog'], 3)), ')',])
        class_ms2query = ''.join([
            str(feature_dicts[ID]['ms2query_results'][0]['npc_class_results']),
            ' (NP Classifier);', '<br>',
            str(feature_dicts[ID]['ms2query_results'][0]['cf_subclass']),
            ' (ClassyFire)'])
        superclass_ms2query = ''.join([str(
            feature_dicts[ID]['ms2query_results'][0]['npc_superclass_results']
        ),
            ' (NP Classifier);', '<br>',
            str(feature_dicts[ID]['ms2query_results'][0]['cf_superclass']),
            ' (ClassyFire)'])

    fold_diff_list = []
    if feature_dicts[ID]['dict_fold_diff'] is not None:
        for comp in feature_dicts[ID]['sorted_fold_diff']:
            if feature_dicts[ID]['dict_fold_diff'][comp] >= 1:
                fold_diff_list.append(''.join([
                    str(feature_dicts[ID]['dict_fold_diff'][comp]),
                    ' (',
                    comp,
                    '),',
                    '<br>',
                ]))
    else:
        fold_diff_list = [None]

    combined_list_int = []
    for i in range(len(feature_dicts[ID]['presence_samples'])):
        combined_list_int.append(''.join([
            str(feature_dicts[ID]['intensities_samples'][i]), ' (',
            str(feature_dicts[ID]['presence_samples'][i]), '),', '<br>', ]))

    combined_list_bio = []
    if feature_dicts[ID]['bioactivity_associated']:
        for i in range(len(feature_dicts[ID]['presence_samples'])):
            combined_list_bio.append(''.join([
                str(feature_dicts[ID]['bioactivity_samples'][i]), ' (',
                str(feature_dicts[ID]['presence_samples'][i]), '),', '<br>',
                ]))
    else:
        combined_list_bio = [None]

    combined_list_orig_bio = []
    if feature_dicts[ID]['bioactivity_associated']:
        for i in range(len(feature_dicts[ID]['presence_samples'])):
            sample = feature_dicts[ID]['presence_samples'][i]
            combined_list_orig_bio.append(''.join([
                str(sample_stats['original_bioactivity'][sample]), ' (',
                str(sample), '),', '<br>',
            ]))
    else:
        combined_list_orig_bio = [None]

    combined_list_adducts = []
    if feature_dicts[ID]['ann_adduct_isotop']:
        for i in range(len(feature_dicts[ID]['ann_adduct_isotop'])):
            combined_list_adducts.append(''.join([
                str(feature_dicts[ID]['ann_adduct_isotop'][i]),
                ',<br>', ]))
    else:
        combined_list_adducts = [None]

    groups_cliques = []
    if feature_dicts[ID]['similarity_clique']:
        for group in feature_dicts[ID]['set_groups_clique']:
            groups_cliques.append(''.join([group, '<br>', ]))
    else:
        groups_cliques = [None]

    sim_clique_len = None
    sim_clique_list = None
    if feature_dicts[ID]['similarity_clique']:
        sim_clique_len = len(
            sample_stats['cliques'][
                str(feature_dicts[ID]['similarity_clique_number'])][0]
            )
        sim_clique_list = (', '.join(str(i) for i in sample_stats['cliques'][
            str(feature_dicts[ID]['similarity_clique_number'])
        ][0]))

    quant_data_ass = False
    quant_data_trend = False
    if feature_dicts[ID]['bioactivity_associated']:
        quant_data_ass = True
        if feature_dicts[ID]['bioactivity_trend']:
            quant_data_trend = True
    separator = '-----'
    data = [
        ['Feature ID', ID],
        ['Precursor <i>m/z</i>', feature_dicts[ID]['precursor_mz']],
        ['Retention time (min)', samples[smpl].at[index, 'retention_time']],
        ['Feature intensity (absolute)', int_sample],
        ['Feature intensity (relative)', round(
            samples[smpl].at[index, 'rel_intensity_score'], 2
        )],
        [separator, separator],
        ['Blank-associated', feature_dicts[ID]['blank_associated']],
        ['Novelty score',
         round(samples[smpl].at[index, 'novelty_score'], 2)],
        ['QuantData-associated', quant_data_ass],
        ['QuantData-trend', quant_data_trend],
        ['Peak overlap (%)', round(
            (samples[smpl].at[index, 'convolutedness_score']*100), 0
        )],
        [separator, separator],
        ['Spectral library: best match', cosine_annotation],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: best match/analog''', ann_ms2query],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: <i>m/z</i> difference to best match/analog''',
         mass_diff_ms2query],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: predicted class of best match/analog''',
         class_ms2query],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: predicted superclass of best match/analog''',
         superclass_ms2query],
        [separator, separator],
        ['Feature found in groups', ("".join(
            f"{i}<br>" for i in feature_dicts[ID]['set_groups']
        ))],
        ['Fold-differences across groups', ("".join(
            str(i) for i in fold_diff_list
        ))],
        ['Intensity per sample (highest to lowest)', ("".join(
            str(i) for i in combined_list_int
        ))],
        ['QuantData per sample (highest to lowest)', ("".join(
            str(i) for i in combined_list_bio
        ))],
        ['Original QuantData (highest to lowest)', ("".join(
            str(i) for i in combined_list_orig_bio
        ))],
        ['Putative adducts', ("".join(str(i) for i in combined_list_adducts))],
        [separator, separator],
        ['Spectral similarity network ID',
         feature_dicts[ID]['similarity_clique_number']],
        ['Groups in network', ("".join(str(i) for i in groups_cliques))],
        ['Number of features in network', sim_clique_len],
        ['IDs of features in network', sim_clique_list],
    ]
    return data


def empty_feature_info_df() -> list:
    '''Generate placeholder table for feature info

    Returns
    -------
    `list`
        List of lists: empty feature info table
    '''
    data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (min)', None],
        ['Feature intensity (absolute)', None],
        ['Feature intensity (relative)', None],
        ['-----', '-----'],
        ['Blank-associated', None],
        ['Novelty score', None],
        ['QuantData-associated', None],
        ['QuantData-trend', None],
        ['Peak overlap (%)', None],
        ['-----', '-----'],
        ['Spectral library: best match', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: <i>m/z</i> difference to best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: predicted class of best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>:predicted superclass of best match/analog''', None],
        ['-----', '-----'],
        ['Feature found in groups', None],
        ['Fold-differences across groups', None],
        ['Intensity per sample (highest to lowest)', None],
        ['QuantData per sample (highest to lowest)', None],
        ['Original QuantData (highest to lowest)', None],
        ['Putative adducts', None],
        ['-----', '-----'],
        ['Spectral similarity network ID', None],
        ['Groups in network', None],
        ['Number of features in network', None],
        ['IDs of features in network', None],
    ]
    return data
