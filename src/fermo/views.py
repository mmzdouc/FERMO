from flask import (
    Blueprint,
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
    empty_loading_table)
views = Blueprint(__name__, "views")


# routing
@views.route("/")
def landing(version=__version__.__version__):
    return render_template('landing.html', version=version)


@views.route("/loading", methods=['GET', 'POST'])
def loading(version=__version__.__version__):
    if request.method == 'POST':
        filename = save_file('sessionFile', 'json')
        if filename:
            return redirect(url_for('views.inspect_uploaded_file',
                                    filename=filename))
        else:
            return redirect(request.url)
    return render_template('loading.html', version=version,
                           table=empty_loading_table())


@views.route("/loading/<filename>")  # for inspecting the uploaded file before submitting it to the dashboard.
def inspect_uploaded_file(filename, version=__version__.__version__):
    table_dict, message = parse_sessionfile(filename, version)
    if message:
        flash(message)
    return render_template('loaded_file.html', version=version,
                           table=table_dict)


@views.route("/dashboard")
def dashboard(version=__version__.__version__):
    return render_template('dashboard.html', version=version)


@views.route("/processing", methods=['GET', 'POST'])
def processing(version=__version__.__version__):
    return render_template('processing.html', version=version)
