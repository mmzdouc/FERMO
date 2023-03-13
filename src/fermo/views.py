from flask import (
    Blueprint,
    render_template,
    request,
)
import fermo.__version__ as __version__

from fermo.app_utils.input_testing import check_file
views = Blueprint(__name__, "views")


# routing
@views.route("/")
def landing(version=__version__.__version__):
    return render_template('landing.html', version=version)


@views.route("/loading", methods=['GET', 'POST'])
def loading(version=__version__.__version__):
    if request.method == 'POST':
        return check_file('sessionFile', 'json')
    return render_template('loading.html', version=version)


@views.route("/loading/<filename>")  # for inspecting the uploaded file before submitting it to the dashboard.
def inspect_uploaded_file(filename, version=__version__.__version__):
    return render_template('loaded_file.html', version=__version__.__version__)


@views.route("/dashboard")
def dashboard(version=__version__.__version__):
    return render_template('dashboard.html', version=__version__.__version__)


@views.route("/processing", methods=['GET', 'POST'])
def processing(version=__version__.__version__):
    return render_template('processing.html', version=__version__.__version__)
