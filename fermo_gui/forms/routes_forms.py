from flask import render_template

from fermo_gui.forms import bp


@bp.route("/")
def start_analysis():
    """Render the index page of the start analysis forms.

    Returns:
        The rendered forms.html page as string
    """
    return render_template("forms/forms.html")
