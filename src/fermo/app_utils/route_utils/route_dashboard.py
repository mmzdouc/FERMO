from fermo.app_utils.dashboard.chromatogram import plot_central_chrom


def sample_changed(
    req,
    sample_stats: dict,
    samples_json_dict: dict,
    feature_dicts: dict,
    vis_features: str,
):
    """ Call all functions that need updating when the sample changed

    Parameters
    ----------
    req: `request object`
    sample_stats: `dict`
    samples_json_dict: `dict`
    feature_dicts: `dict`
    vis_features: `str`

    Returns
    -------
    response: `dict`
    """
    samplename = req['sample'][1]
    feature_index = None
    chromatogram = plot_central_chrom(
        samplename,
        feature_index,
        sample_stats,
        samples_json_dict,
        feature_dicts,
        vis_features,
    )
    response = {"chromatogram": chromatogram}
    return response
