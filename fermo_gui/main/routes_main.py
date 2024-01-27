from flask import render_template

from fermo_gui.main import bp


@bp.route("/")
def index():
    """Render the index (landing) page of fermo_gui

    Returns:
        The index.html page as string.
    """
    return render_template("index.html")
