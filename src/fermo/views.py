from flask import (
    Blueprint,
    render_template,
    flash, redirect,
    current_app,  # allows to access the config elements
    request,
    url_for
)
import __version__
# import config
from werkzeug.utils import secure_filename
import os

views = Blueprint(__name__, "views")


def allowed_file(filename):
    """ Returns boolean for valid filenames and allowed extensions"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
        current_app.config.get('ALLOWED_EXTENSION')


# routing
@views.route("/")
def landing(version=__version__.__version__):
    return render_template('landing.html', version=version)


@views.route("/loading", methods=['GET', 'POST'])
def loading(version=__version__.__version__):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'sessionFile' not in request.files:  # todo: how should this \situation really be handled? 
            return redirect(request.url)
        file = request.files['sessionFile']  # 'sessionFile' is taken from the name-attribute of the corresponding input form in the template
        if file.filename == '':  # if the user doesn't choose a file the browser submits an emtpy file without a name
            flash('No file was loaded. Please upload a session-file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename.endswith('json'):
                try:
                    file.save(os.path.join('src/fermo/uploads/', filename))
                except FileNotFoundError:
                    print("file or folder didn't exist, so the uploaded file couldn't be saved")
                return redirect(url_for('views.inspect_uploaded_file',
                                        filename=filename))
            else:
                flash("File must be a json-file!")
                return redirect(request.url)
    return render_template('loading.html', version=version)


@views.route("/loading/<filename>")  # for inspecting the uploaded file before submitting it to the dashboard.
def inspect_uploaded_file(filename, version=__version__.__version__):
    return render_template('loaded_file.html', version=__version__.__version__)


@views.route("/dashboard")
def dashboard(version=__version__.__version__):
    return render_template('dashboard.html', version=__version__.__version__)


@views.route("/processing")
def processing(version=__version__.__version__):
    return render_template('processing.html', version=__version__.__version__)
