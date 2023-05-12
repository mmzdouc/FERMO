from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from fermo.__version__ import __version__
from fermo.app_utils.dashboard.networking_graph import (
    collect_edgedata,
    collect_nodedata,
    generate_cyto_elements,
)
from fermo.app_utils.input_testing import (
    save_file,
    parse_sessionfile,
    empty_loading_table,
)
from fermo.app_utils.dashboard.dashboard_functions import (
    access_loaded_data,
    load_example,
)
from fermo.app_utils.dashboard.chromatogram import (
    placeholder_graph,
    plot_central_chrom,
    plot_clique_chrom,
)
from fermo.app_utils.dashboard.feature_table import (
    empty_feature_info_df,
    update_feature_table,
)
from fermo.app_utils.dashboard.sample_table import (
    get_samples_overview,
    get_samples_statistics,
)
from fermo.app_utils.dashboard.networking_graph import stylesheet_cytoscape
from fermo.app_utils.route_utils.route_dashboard import (
    feature_changed,
    sample_changed,
)

views = Blueprint(__name__, "views")


# routing
@views.route("/")
def landing(version=__version__):
    return render_template('landing.html', version=version)


@views.route("/loading", methods=['GET', 'POST'])
def loading(version=__version__):
    ''' Handle requests on the loading page

    Parameters
    ----------
    version: `str`

    Returns
    -------
    `str` or `flask.wrappers.Response`
        either the html for the initial loading page, or the response to the
        request

    Notes
    -----
    Displays the initial loading page, or if a session file was uploaded,
    checks if it was transmitted via the request, then accesses the file from
    the request-object, allowed extensions and upload folder from the config
    and saves the file in the specified location. Then redirects to the loading
    page that displays the file-overview table. If applicable, displays a
    warning message for missing or (possibly) incompatible input.
    '''
    if request.method == 'POST':
        if 'sessionFile' not in request.files:
            print('Input ID was not in the request')
        else:
            sessionfile = request.files['sessionFile']
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
            feedback_or_filename, file_saved = save_file(
                sessionfile,
                'json',
                upload_folder,
            )
            if file_saved:
                filename = feedback_or_filename
                return redirect(url_for(
                    'views.inspect_uploaded_file',
                    filename=filename,
                ))
            else:
                feedback = feedback_or_filename
                flash(feedback)
                return redirect(request.url)
    else:
        return render_template(
            'loading.html',
            version=version,
            table=empty_loading_table(),
        )


@views.route("/loading/<filename>", methods=['GET', 'POST'])
def inspect_uploaded_file(filename, version=__version__):
    '''Display session file overview

    Parameters
    ----------
    filename: `str`
    version: `str`

    Returns
    -------
    `str` or `flask.wrappers.Response`
        either the html for the initial loading page, or the response to the
        request

    Notes
    -----
    Displays the sessionfile overview and determines the behavior after button
    clicks when a file was uploaded:
    - if file-upload button was clicked, redirect to loading() while keeping
    the POST method (hence code 307)
    - if Start_FERMO_Dashboard-Button was clicked, #doSomething and redirect to
    dashboard()
    '''
    if request.method == 'POST':
        try:
            request.form['Start_FERMO_Dashboard']
        except KeyError:
            return redirect(url_for('views.loading'), code=307)
        else:
            # to be implemented: parse the sessionfile as needed for the
            # dashboard
            return redirect(url_for('views.dashboard'))
    else:
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        table_dict, message = parse_sessionfile(
            filename,
            version,
            upload_folder,
        )
        if message:
            flash(message)
        return render_template(
            'loading.html',
            version=version,
            table=table_dict,
        )


@views.route("/processing", methods=['GET', 'POST'])
def processing(version=__version__):
    if request.method == 'POST':
        filename = save_file([
            'peaktableFile',
            'MSMSFile',
            'quantDataFile',
            'MetadataFile',
            'spectralLibraryFile',
        ])
        if filename:
            pass
    return render_template('processing.html', version=version)


@views.route("/dashboard")
def dashboard(version=__version__):
    '''Render dashboard page'''
    # load data for placeholder main chromatogram
    graphJSON = placeholder_graph()
    feature_table = empty_feature_info_df()

    return render_template(
        'dashboard.html',
        version=version,
        general_sample_table=[[]],
        specific_sample_table=[[]],
        feature_table=feature_table,
        graphJSON=graphJSON,
        networkJSON=None,
        cytoscape_message=None,
        cyto_stylesheetJSON=None,
        node_table=[[]],
        edge_table=[[]],
        samplename=None,
    )


@views.route("/example", methods=['GET', 'POST'])
def example(version=__version__):
    '''Example dashboard'''
    data = load_example('example_data/FERMO_session.json')
    if data:
        (sample_stats,
         samples_json_dict,
         samples_dict,
         feature_dicts,
         ) = access_loaded_data(data)
        cyto_stylesheet = stylesheet_cytoscape()

        if request.method == 'GET':
            # hardcode some variables to display as default
            samplename = list(samples_dict)[0]
            active_feature_index = None
            active_feature_id = None
            nodedata = {}
            edgedata = {}

            general_sample_table = get_samples_statistics(
                samples_json_dict,
                samples_dict,
                feature_dicts,
            )
            sample_overview_table = get_samples_overview(
                sample_stats,
                samples_json_dict,
                samples_dict,
                feature_dicts,
            )
            chromatogram = plot_central_chrom(
                samplename,
                active_feature_index,
                sample_stats,
                samples_json_dict,
                feature_dicts,
                "ALL",
            )
            clique_chromatogram = plot_clique_chrom(
                samplename,
                active_feature_index,
                active_feature_index,
                sample_stats,
                samples_json_dict,
                feature_dicts,
            )
            feature_table = update_feature_table(
                samplename,
                feature_dicts,
                samples_json_dict,
                sample_stats,
                active_feature_id,
                active_feature_index
            )
            network, cytoscape_message = generate_cyto_elements(
                samplename,
                active_feature_id,
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
                samplename=samplename
            )

        else:  # method == 'POST'
            req = request.get_json()
            vis_features = "ALL"  # should be taken from response: User
            # selection from filter panel "Visualize features" radio buttons

            # parse the request
            if req['sample'][0]:  # i.e. if sample has changed
                resp = sample_changed(
                    req,
                    sample_stats,
                    samples_json_dict,
                    feature_dicts,
                    vis_features,
                )

            elif req['featChanged']:  # i.e. there is an active feature
                resp = feature_changed(
                    req,
                    feature_dicts,
                    samples_json_dict,
                    sample_stats,
                    vis_features,
                )
                # resp = json.dumps(resp)
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
