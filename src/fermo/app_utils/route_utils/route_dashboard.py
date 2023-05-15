import json
from fermo.app_utils.dashboard.chromatogram import (
    plot_central_chrom,
    plot_clique_chrom,
)
from fermo.app_utils.dashboard.feature_table import update_feature_table
from fermo.app_utils.dashboard.cytoscape_graph import (
    collect_edgedata,
    collect_nodedata,
    generate_cyto_elements,
)


def sample_changed(
    req: dict,
    sample_stats: dict,
    samples_json_dict: dict,
    feature_dicts: dict,
    vis_features: str,
):
    """ Call all functions that need updating when the sample changed

    Parameters
    ----------
    req: `dict`
        as returned by request.get_json()
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
    feature_id = None
    nodedata = {}
    edgedata = {}
    chromatogram = plot_central_chrom(
        samplename,
        feature_index,
        sample_stats,
        samples_json_dict,
        feature_dicts,
        vis_features,
    )
    clique_chrom = plot_clique_chrom(
        samplename,
        feature_index,
        feature_id,
        sample_stats,
        samples_json_dict,
        feature_dicts,
    )
    feature_table = update_feature_table(
        samplename,
        feature_dicts,
        samples_json_dict,
        sample_stats,
        feature_id,
        feature_index
    )
    network, cytoscape_message = generate_cyto_elements(
        samplename,
        feature_id,
        feature_dicts,
        sample_stats,
    )
    node_table = collect_nodedata(
        nodedata,
        feature_dicts,
    )
    edge_table = collect_edgedata(edgedata)
    response = {
        "chromatogram": chromatogram,
        "cliqueChrom": clique_chrom,
        "featTable": str(feature_table),
        "network": network,
        "cytoscapeMessage": json.dumps(cytoscape_message),
        "nodeTable": json.dumps(node_table),
        "edgeTable": json.dumps(edge_table)
    }
    return response


def feature_changed(
    req: dict,
    feature_dicts: dict,
    samples_json_dict: dict,
    sample_stats: dict,
    vis_features: str
):
    """ Call all functions that need updating when a new feature was selected

    Parameters
    ----------
    req: `dict`
        as returned by request.get_json()
    feature_dicts: `dict`
    samples_json_dict: `dict`
    sample_stats: `dict`
    vis_features: `str`

    Returns
    -------
    response: `dict`

    Notes
    -----
    If featID is in the response, the feature was selected in the
    cytoscape graph. This graph then does not need to be updated, therefore
    generate_cyto_elements() is not called.
    """
    samplename = req['sample'][1]
    resp = {}
    if 'featIndex' in req:  # feature was selected in the chromatogram
        feature_index = int(req['featIndex'])
        feature_id = samples_json_dict[samplename]['feature_ID'][feature_index]
        network, cytoscape_message = generate_cyto_elements(
            samplename,
            feature_id,
            feature_dicts,
            sample_stats,
        )
        resp.update({
            "network": network,
            "cytoscapeMessage": json.dumps(cytoscape_message),
        })

    else:  # feature was selected in the cytoscape graph
        feature_id = int(req['featID'])
        samples_df = samples_json_dict[samplename]
        try:
            feature_index = int(samples_df.index[
                samples_df.feature_ID == feature_id
            ][0])
        except IndexError:  # selected feature is not in the active sample
            return resp
    chromatogram = plot_central_chrom(
        samplename,
        feature_index,
        sample_stats,
        samples_json_dict,
        feature_dicts,
        vis_features,
    )
    clique_chrom = plot_clique_chrom(
        samplename,
        feature_index,
        feature_id,
        sample_stats,
        samples_json_dict,
        feature_dicts,
    )
    feature_table = update_feature_table(  # convert to string to avoid bug
        samplename,
        feature_dicts,
        samples_json_dict,
        sample_stats,
        feature_id,
        feature_index,
    )

    resp.update({
        "chromatogram": chromatogram,
        "cliqueChrom": clique_chrom,
        "featTable": str(feature_table),
    })
    return resp
