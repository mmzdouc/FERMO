from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from __version__ import __version__
from app_utils.dashboard.cytoscape_graph import (
    collect_edgedata,
    collect_nodedata,
    generate_cyto_elements,
)

from app_utils.dashboard.dashboard_functions import (
    access_loaded_data,
    default_filters,
    load_sessionFile,
)
from app_utils.dashboard.chromatogram import (
    plot_central_chrom,
    plot_clique_chrom,
)
from app_utils.dashboard.feature_table import (
    update_feature_table,
)
from app_utils.dashboard.sample_table import (
    get_samples_overview,
    get_samples_statistics,
)
from app_utils.dashboard.cytoscape_graph import stylesheet_cytoscape
from app_utils.route_utils.route_dashboard import (
    feature_changed,
    filters_changed,
    sample_changed,
)

views = Blueprint(__name__, "views")


# routing
@views.route("/")
def landing(version=__version__):
    return redirect(url_for('views.example'))


@views.route("/example", methods=['GET', 'POST'])
def example(version=__version__):
    '''Example dashboard

    Parameters
    ----------
    version: `str`

    Returns
    -------
    `str`
        html for the browser to render
    or `flask.wrappers.Response`
        response for the browser to handle after fetch

    Notes
    -----
    Displays the dashboard with example data. If a request is received,
    (user clicks on something), the request is handled depending on what was
    clicked.
    There are three major types of requests:
    - filters were applied
    - a sample was selected
    - a feature was selected\n
    Each request calls a separate function in route_utils/route_dashboard.py
    to be handled appropriately.
    '''
    data = load_sessionFile('example_data/FERMO_session.json')
    if data:
        (sample_stats,
         samples_json_dict,
         samples_dict,
         feature_dicts,
         ) = access_loaded_data(data)
        cyto_stylesheet = stylesheet_cytoscape()

        if request.method == 'GET':
            # set default variables
            session['samplename'] = list(samples_dict)[0]
            session['vis_features'] = 'ALL'
            session['active_feature_index'] = None
            session['active_feature_id'] = None
            session['thresholds'] = default_filters()
            nodedata = {}
            edgedata = {}

            general_sample_table = get_samples_statistics(
                samples_json_dict,
                samples_dict,
                feature_dicts,
                session['thresholds'],
            )
            sample_overview_table = get_samples_overview(
                sample_stats,
                samples_json_dict,
                samples_dict,
                feature_dicts,
                session['thresholds'],
            )
            chromatogram = plot_central_chrom(
                session['samplename'],
                session['active_feature_index'],
                sample_stats,
                samples_json_dict,
                feature_dicts,
                session['vis_features'],
                session['thresholds']
            )
            clique_chromatogram = plot_clique_chrom(
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

            return render_template(
                'dashboard.html',
                version=version,
                general_sample_table=general_sample_table,
                specific_sample_table=sample_overview_table,
                feature_table=feature_table,
                graphJSON=chromatogram,
                cliqueChromJSON=clique_chromatogram,
                networkJSON=network,
                cytoscape_message=cytoscape_message,
                cyto_stylesheetJSON=cyto_stylesheet,
                node_table=node_table,
                edge_table=edge_table,
                samplename=session['samplename']
            )

        else:  # method == 'POST'
            req = request.get_json()
            if 'featureVisualizationOptions' in req:  # filters were used
                resp = filters_changed(
                    req,
                    sample_stats,
                    samples_json_dict,
                    feature_dicts,
                    samples_dict,
                )

            elif 'sample' in req:
                # parse the request
                if req['sample'][0]:  # i.e. if sample has changed
                    resp = sample_changed(
                        req,
                        sample_stats,
                        samples_json_dict,
                        feature_dicts,
                        session['vis_features'],
                    )

                elif req['featChanged']:  # i.e. there is an active feature
                    resp = feature_changed(
                        req,
                        feature_dicts,
                        samples_json_dict,
                        sample_stats,
                        session['vis_features'],
                    )
                else:
                    try:
                        edge_data = req['edgeData']
                    except KeyError:
                        try:
                            node_data = req['nodeData']
                        except KeyError:
                            resp = {}
                        else:
                            resp = collect_nodedata(node_data, feature_dicts)
                    else:
                        resp = collect_edgedata(edge_data)
            return resp

    else:  # data could not be loaded
        flash('Example data could not be loaded')
        return render_template(
            'dashboard.html',
            version=version,
            general_sample_table=[],
            specific_sample_table=[],
            feature_table=[],
        )
