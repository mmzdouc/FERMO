import json
from flask import session
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


def filters_changed():
    pass


def sample_changed(
    req: dict,
    sample_stats: dict,
    samples_json_dict: dict,
    feature_dicts: dict,
    vis_features: str,
) -> dict:
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
    session['samplename'] = req['sample'][1]
    session['active_feature_index'] = None
    session['active_feature_id'] = None
    nodedata = {}
    edgedata = {}
    chromatogram = plot_central_chrom(
        session['samplename'],
        session['active_feature_index'],
        sample_stats,
        samples_json_dict,
        feature_dicts,
        vis_features,
    )
    clique_chrom = plot_clique_chrom(
        session['samplename'],
        session['active_feature_index'],
        session['active_feature_id'],
        sample_stats,
        samples_json_dict,
        feature_dicts,
    )
    feature_table = update_feature_table(
        session['samplename'],
        feature_dicts,
        samples_json_dict,
        sample_stats,
        session['active_feature_id'],
        session['active_feature_index']
    )
    network, cytoscape_message = generate_cyto_elements(
        session['samplename'],
        session['active_feature_id'],
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
) -> dict:
    """ Call all functions that need updating when a new feature was selected,\n
    depending on where the feature was selected (chromatogram or network-graph)

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
    session['samplename'] = req['sample'][1]
    resp = {}
    if 'featIndex' in req:  # feature was selected in the chromatogram
        session['active_feature_index'] = int(req['featIndex'])
        session['active_feature_id'] = int(
            samples_json_dict[session['samplename']]
                             ['feature_ID']
                             [session['active_feature_index']]
        )

    else:  # feature was selected in the cytoscape graph
        session['active_feature_id'] = int(req['featID'])
        samples_df = samples_json_dict[session['samplename']]
        try:
            session['active_feature_index'] = int(samples_df.index[
                samples_df.feature_ID == session['active_feature_id']
            ][0])
        except IndexError:  # selected feature is not in the active sample
            return resp
    chromatogram = plot_central_chrom(
        session['samplename'],
        session['active_feature_index'],
        sample_stats,
        samples_json_dict,
        feature_dicts,
        vis_features,
    )
    clique_chrom = plot_clique_chrom(
        session['samplename'],
        session['active_feature_index'],
        session['active_feature_id'],
        sample_stats,
        samples_json_dict,
        feature_dicts,
    )
    feature_table = update_feature_table(  # convert to string to avoid bug
        session['samplename'],
        feature_dicts,
        samples_json_dict,
        sample_stats,
        session['active_feature_id'],
        session['active_feature_index'],
    )
    network, cytoscape_message = generate_cyto_elements(
            session['samplename'],
            session['active_feature_id'],
            feature_dicts,
            sample_stats,
        )
    resp.update({
        "chromatogram": chromatogram,
        "cliqueChrom": clique_chrom,
        "featTable": str(feature_table),
        "network": network,
        "cytoscapeMessage": json.dumps(cytoscape_message),
    })

    return resp
