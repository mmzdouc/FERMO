import json
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
from fermo.app_utils.dashboard_functions import (
    load_example,
    placeholder_graph,
    get_samples_stats,
)
from fermo.app_utils.input_testing import (
    save_file,
    parse_sessionfile,
    empty_loading_table,
)
from fermo.app_utils.dashboard_functions import empty_feature_info_df

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
            allowed_extensions = current_app.config.get('ALLOWED_EXTENSION')
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
            feedback_or_filename, file_saved = save_file(
                sessionfile,
                '.json',
                allowed_extensions,
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
    )


@views.route("/example")
def example(version=__version__):
    '''Example dashboard'''
    data = load_example('example_data/FERMO_session.json')
    if data:
        general_sample_table = get_samples_stats(data)
        specific_sample_table = [[]]
        feature_table = empty_feature_info_df()

        return render_template(
            'dashboard.html',
            version=version,
            general_sample_table=general_sample_table,
            specific_sample_table=specific_sample_table,
            feature_table=feature_table,
            graphJson=json.dumps(data),
        )
    else:
        return render_template(
            'dashboard.html',
            version=version,
            general_sample_table=[],
            specific_sample_table=[],
            feature_table=[],
            )
