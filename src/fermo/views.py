from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import fermo.__version__ as __version__
from fermo.app_utils.input_testing import (
    save_file,
    parse_sessionfile,
    empty_loading_table,
)

views = Blueprint(__name__, "views")


# routing
@views.route("/")
def landing(version=__version__.__version__):
    return render_template('landing.html', version=version)


@views.route("/loading", methods=['GET', 'POST'])
def loading(version=__version__.__version__):
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
            message, filename = save_file(
                sessionfile,
                '.json',
                allowed_extensions,
                upload_folder
            )
            if filename:
                return redirect(url_for(
                    'views.inspect_uploaded_file',
                    filename=filename
                ))
            else:
                flash(message)
                return redirect(request.url)
    return render_template(
        'loading.html',
        version=version,
        table=empty_loading_table()
    )


@views.route("/loading/<filename>")
def inspect_uploaded_file(filename, version=__version__.__version__):
    '''Display session file overview 
    (and to be implemented: redirect to dashboard page)
    '''
    table_dict, message = parse_sessionfile(filename, version)
    if message:
        flash(message)
    return render_template(
        'loaded_file.html',
        version=version,
        table=table_dict,
    )


@views.route("/processing", methods=['GET', 'POST'])
def processing(version=__version__.__version__):
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
def dashboard(version=__version__.__version__):
    return render_template('dashboard.html', version=version)
