from statistics import StatisticsError, mean

from fermo.app_utils.dashboard.dashboard_functions import (
    generate_subsets,
)


def get_samples_statistics(
    samples_json_dict: dict,
    samples_dict: dict,
    feature_dicts: dict,
    thresholds: dict,
) -> list:
    '''Generate list of lists for sample stats

    Parameters
    ----------
    samples_json_dict: `dict`
    samples_dict: `dict`
    feature_dicts: `dict`
    thresholds: `dict`

    Returns
    -------
    `list`
        List of lists: sample stats table
    '''
    selected_features = set()
    blank_features = set()
    nonblank_features = set()
    selected_cliques = set()
    filtered_samples = {}

    # loop over samples to access info like selected features for each sample
    for sample in samples_dict:
        # apply filters
        filtered_samples[sample] = generate_subsets(
            samples_json_dict,
            sample,
            thresholds,
            feature_dicts
        )
        # find samples with certain characteristics, e.g. nonblank, among the
        # selected
        selected_features.update(
            set(filtered_samples[sample]['all_select_no_blank'])
        )
        blank_features.update(set(filtered_samples[sample]['blank_ms1']))
        nonblank_features.update(set(filtered_samples[sample]['all_nonblank']))
        for ID in selected_features:
            if feature_dicts[str(ID)]['similarity_clique']:
                selected_cliques.add(
                    feature_dicts[str(ID)]['similarity_clique_number']
                )
    n_samples = len(samples_dict)
    n_features = len(feature_dicts)
    n_selected_features = len(selected_features)
    n_selected_cliques = len(selected_cliques)
    n_nonblank_features = len(nonblank_features)
    n_blank_features = len(blank_features)
    stats_list = [
        n_samples,
        n_features,
        n_selected_features,
        n_selected_cliques,
        n_nonblank_features,
        n_blank_features,
    ]
    return stats_list


def get_samples_overview(
    sample_stats: dict,
    samples_json_dict: dict,
    samples_dict: dict,
    feature_dicts: dict,
    thresholds: dict,
) -> list:
    '''Generate list of lists for sample overview

    Parameters
    ----------
    sample_stats: `dict`\n
    samples_json_dict: `dict`\n
    samples_dict: `dict`\n
    feature_dicts: `dict`\n
    thresholds: `dict`\n

    Returns
    -------
    `list`
        List of lists: sample overview table
    '''
    samples_table = []
    filtered_samples = {}
    for sample in samples_dict:
        filtered_samples[sample] = generate_subsets(
            samples_json_dict,
            sample,
            thresholds,
            feature_dicts
        )
        sample_row = [sample]

        # access/create values for sample overview table
        group = samples_dict[sample]
        n_selected_features = len(
            filtered_samples[sample]['all_select_no_blank']
        )
        n_selected_networks = len(calc_selected_networks(
            sample,
            filtered_samples,
            feature_dicts,
        ))
        div_score = calc_diversity_score(sample, sample_stats)
        spec_score = calc_specificity_score(
            sample,
            sample_stats,
            filtered_samples,
            feature_dicts,
        )
        nov_score = calc_sample_mean_novelty(
            sample,
            feature_dicts,
            filtered_samples,
        )
        n_all_selected_features = len(filtered_samples[sample]['all_features'])
        n_non_blank = len(filtered_samples[sample]['all_nonblank'])
        n_blank = len(filtered_samples[sample]['blank_ms1'])

        # append results to sample row
        sample_row.append(group)
        sample_row.append(n_selected_features)
        sample_row.append(n_selected_networks)
        sample_row.append(div_score)
        sample_row.append(spec_score)
        sample_row.append(nov_score)
        sample_row.append(n_all_selected_features)
        sample_row.append(n_non_blank)
        sample_row.append(n_blank)

        # append sample row to samples table before moving on to next sample
        samples_table.append(sample_row)
    return samples_table


def calc_selected_networks(
    sample: str,
    filtered_samples: dict,
    feature_dicts: dict,
) -> list:
    '''Calculate selected cliques for given sample

    Parameters
    ----------
    sample: `str`\n
    filtered_samples: `dict`\n
    feature_dicts: `dict`

    Returns
    -------
    sample_selected_cliques: `list`
    '''
    sample_selected_cliques = []
    for ID in filtered_samples[sample]['all_select_no_blank']:
        if feature_dicts[str(ID)]['similarity_clique']:
            sample_selected_cliques.append(
                feature_dicts[str(ID)]['similarity_clique_number']
            )
    return sample_selected_cliques


def calc_diversity_score(
    sample: str,
    sample_stats: dict,
) -> int:
    '''Calculate diversity scores for each sample

    Parameters
    ----------
    sample: `str`\n
    sample_stats: `dict`

    Returns
    -------
    div_scores: `int`
    '''
    try:
        div_score = round((len(set(
            sample_stats["cliques_per_sample"][sample]
        ).difference(
            set(sample_stats["set_blank_cliques"]))
        )/len(
            set(sample_stats["set_all_cliques"]).difference(
                set(sample_stats["set_blank_cliques"])
            )
        )
        ), 2)
    except (ZeroDivisionError, StatisticsError):
        div_score = 0
    return div_score


def calc_specificity_score(
    sample: str,
    sample_stats: dict,
    filtered_samples: dict,
    feature_dicts: dict,
) -> int:
    '''Calculate specificity scores for a sample

    Parameters
    ----------
    sample: `str`\n
    sample_stats: `dict`\n
    filtered_samples: `dict`\n
    feature_dicts: `dict`

    Returns
    -------
    spec_score : `int`
    '''
    unique_cliques = set()
    for ID in filtered_samples[sample]['all_nonblank']:
        if ((
            len(feature_dicts[str(ID)]['set_groups_clique']) == 1
        ) and (
            sample in feature_dicts[str(ID)]['presence_samples']
        )):
            unique_cliques.add(
                feature_dicts[str(ID)]['similarity_clique_number']
            )
    try:
        spec_score = round(((len(
            unique_cliques
        ))/len(set(
            sample_stats["cliques_per_sample"][sample]
        ).difference(
            set(sample_stats["set_blank_cliques"])
        ))), 2)
    except ZeroDivisionError:
        spec_score = 0
    return spec_score


def calc_sample_mean_novelty(
    sample: str,
    feature_dicts: dict,
    filtered_samples: dict,
) -> int:
    '''Calculate unique cliques per sample

    Parameters
    ----------
    sample: `str`\n
    feature_dicts: `dict`\n
    filtered_samples: `dict`

    Returns
    -------
    sample_mean_novelty: `int`

    Notes
    -----
    statistics.mean() throws error if any None in list
    '''
    list_novelty_scores = []
    for ID in filtered_samples[sample]['all_nonblank']:
        nov_score = feature_dicts[str(ID)]['novelty_score']
        if isinstance(nov_score, int) or isinstance(nov_score, float):
            list_novelty_scores.append(nov_score)
    try:
        sample_mean_novelty = round(mean(list_novelty_scores), 2)
    except StatisticsError:
        sample_mean_novelty = 0

    return sample_mean_novelty
