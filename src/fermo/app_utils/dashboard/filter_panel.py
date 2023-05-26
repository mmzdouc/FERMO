def read_threshold_values(
    req: dict,
) -> dict:
    '''Bundle filter values into dict

    Parameters
    ----------
    req: `dict`

    Returns
    ------
    `dict`

    Notes
    -----
    int and float values must be tested for None.
    '''
    # extract data from request
    blank_designation_toggle = req['BlankFeaturesOptions']
    novelty_threshold = [float(req['fromNovelty']), float(req['toNovelty'])]
    rel_intensity_threshold = [float(req['fromRelInt']), float(req['toRelInt'])]
    peak_overlap_threshold = [float(req['fromPeak']), float(req['toPeak'])]
    bioactivity_threshold = req['quantDataAssociation']
    filter_adduct_isotopes = req['adductSearch']
    filter_annotation = req['annotationSearch']
    filter_feature_id = req['featureIdSearch']
    filter_spectral_sim_netw = req['specNetIdSearch']
    filter_group = req['groupFeatures']
    filter_group_cliques = req['groupNetworks']
    filter_samplename = req['sampleNameSearch']
    filter_samplenumber_min = req['minSamples']
    filter_samplenumber_max = req['maxSamples']
    filter_precursor_min = req['minMass']
    filter_precursor_max = req['maxMass']
    filter_fold_greater_int = req['fcIncludeNumber']
    filter_fold_greater_regex = req['fcIncludeGroup']
    filter_fold_greater_exclude_int = req['fcExcludeNumber']
    filter_fold_greater_exclude_regex = req['fcExcludeGroup']

    # check for None values
    if filter_feature_id is None:
        filter_feature_id = ''
    if filter_spectral_sim_netw is None:
        filter_spectral_sim_netw = ''
    if filter_precursor_min is None:
        filter_precursor_min = ''
    if filter_precursor_max is None:
        filter_precursor_max = ''
    if filter_samplenumber_min is None:
        filter_samplenumber_min = ''
    if filter_samplenumber_max is None:
        filter_samplenumber_max = ''
    if filter_fold_greater_int is None:
        filter_fold_greater_int = ''
    if filter_fold_greater_exclude_int is None:
        filter_fold_greater_exclude_int = ''

    if None not in [
        rel_intensity_threshold,
        filter_adduct_isotopes,
        bioactivity_threshold,
        novelty_threshold,
        filter_annotation,
        filter_feature_id,
        filter_precursor_min,
        filter_precursor_max,
        filter_spectral_sim_netw,
        filter_group,
        filter_group_cliques,
        peak_overlap_threshold,
        filter_samplename,
        filter_samplenumber_min,
        filter_samplenumber_max,
        blank_designation_toggle,
        filter_fold_greater_int,
        filter_fold_greater_regex,
        filter_fold_greater_exclude_int,
        filter_fold_greater_exclude_regex,
    ]:
        return {
            'rel_intensity_threshold': rel_intensity_threshold,
            'filter_adduct_isotopes': str(filter_adduct_isotopes),
            'quant_biological_value': bioactivity_threshold,
            'novelty_threshold': novelty_threshold,
            'filter_annotation': filter_annotation,
            'filter_feature_id': filter_feature_id,
            'filter_precursor_min': filter_precursor_min,
            'filter_precursor_max': filter_precursor_max,
            'filter_spectral_sim_netw': filter_spectral_sim_netw,
            'filter_group': filter_group,
            'filter_group_cliques': filter_group_cliques,
            'peak_overlap_threshold': peak_overlap_threshold,
            'filter_samplename': filter_samplename,
            'filter_samplenumber_min': filter_samplenumber_min,
            'filter_samplenumber_max': filter_samplenumber_max,
            'blank_designation_toggle': blank_designation_toggle,
            'filter_fold_greater_int': filter_fold_greater_int,
            'filter_fold_greater_regex': filter_fold_greater_regex,
            'filter_fold_greater_exclude_int': filter_fold_greater_exclude_int,
            'filter_fold_greater_exclude_regex':
            filter_fold_greater_exclude_regex,
        }
    else:
        return {}
