from fermo.app_utils.dashboard.chromatogram import plot_central_chrom
from fermo.app_utils.dashboard.feature_table import update_feature_table
from fermo.app_utils.dashboard.networking_graph import (
    collect_edgedata,
    collect_nodedata,
    generate_cyto_elements,
)


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
        "featTable": feature_table,
        "network": network,
        "cytoscapeMessage": cytoscape_message,
        "nodeTable": node_table,
        "edgeTable": edge_table
    }
    return response
