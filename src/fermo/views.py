from flask import Blueprint, render_template
import __version__ 

views= Blueprint(__name__, "views")

@views.route("/")
def landing(version=__version__.__version__):
    return render_template('landing.html', version=version)

@views.route("/loading")
def loading(version=__version__.__version__):
    return render_template('loading.html', version=version)


@views.route("/dashboard")
def dashboard(version=__version__.__version__):
    return render_template('dashboard.html', version=__version__.__version__)


@views.route("/processing")
def processing(version=__version__.__version__):
    return render_template('processing.html', version=__version__.__version__)

