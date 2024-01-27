from flask import render_template

from fermo_gui.main import bp


@bp.route("/")
def index():
    """Set route to the index template."""
    return render_template("index.html")
